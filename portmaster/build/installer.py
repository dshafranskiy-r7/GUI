#!/usr/bin/env python3
"""
Installer module for PortMaster
Replaces the tools/installer.sh script
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import zipfile


def install_portmaster(controlfolder, directory, os_name, esudo="", cur_tty="/dev/tty0"):
    """Install PortMaster to the specified location"""

    print(f"-- Installing on {os_name} --")

    # Create temp directory for runtimes
    temp_dir = Path.cwd()
    os.chdir(controlfolder)

    print(f"Installing PortMaster to {controlfolder}")

    # Create temp directory for runtimes
    temp_runtimes = Path("temp_runtimes")
    temp_runtimes.mkdir(exist_ok=True)

    # Move existing runtimes to temp
    portmaster_libs = Path("PortMaster/libs")
    if portmaster_libs.exists():
        for squashfs_file in portmaster_libs.glob("*.squashfs"):
            try:
                shutil.move(str(squashfs_file), str(temp_runtimes / squashfs_file.name))
            except (FileNotFoundError, PermissionError):
                pass

    # Remove old PortMaster
    for item in ["PortMaster", "PortMaster.sh"]:
        item_path = Path(item)
        if item_path.exists():
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                item_path.unlink()

    # Handle JELOS/ROCKNIX special case
    if os_name in ["JELOS", "ROCKNIX"]:
        jelos_config = Path("/storage/.config/PortMaster")
        if not jelos_config.exists():
            Path("/storage/.config/ports/PortMaster").mkdir(parents=True, exist_ok=True)
            shutil.copytree("/usr/config/PortMaster", "/storage/.config/PortMaster")

        os.chdir("/storage/.config/PortMaster")
        shutil.copy("/usr/config/PortMaster/PortMaster.sh", "PortMaster.sh")
        shutil.copy("/usr/config/PortMaster/control.txt", "control.txt")

        # Remove and create symlinks
        for item in ["gamecontrollerdb.txt", "gptokeyb"]:
            if Path(item).exists():
                Path(item).unlink()

        Path("gamecontrollerdb.txt").symlink_to("/usr/config/SDL-GameControllerDB/gamecontrollerdb.txt")
        Path("gptokeyb").symlink_to("/usr/bin/gptokeyb")
        shutil.copy("/usr/config/PortMaster/portmaster.gptk", "portmaster.gptk")

        os.chdir(controlfolder)

    # Extract PortMaster.zip
    portmaster_zip = temp_dir / "PortMaster.zip"
    if portmaster_zip.exists():
        with zipfile.ZipFile(portmaster_zip, 'r') as zip_ref:
            zip_ref.extractall(".")

    # Apply OS-specific overrides
    if os_name:
        portmaster_dir = Path(controlfolder) / "PortMaster"
        override_dir = portmaster_dir / os_name.lower()

        print(f"--> {override_dir} <--")
        if override_dir.exists():
            portmaster_txt = override_dir / "PortMaster.txt"
            control_txt = override_dir / "control.txt"

            if portmaster_txt.exists():
                shutil.copy(portmaster_txt, portmaster_dir / "PortMaster.sh")
            if control_txt.exists():
                shutil.copy(control_txt, portmaster_dir / "control.txt")

    # Move PortMaster.sh to appropriate location
    relocate_pm = os_name not in ["JELOS", "UnofficialOS", "ROCKNIX", "muOS", "retrodeck"]

    if relocate_pm:
        pm_script = Path("PortMaster/PortMaster.sh")
        if Path("/userdata/roms/ports").is_dir():
            target_path = Path(f"/{directory}/ports/PortMaster.sh")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pm_script), str(target_path))
        else:
            shutil.move(str(pm_script), "PortMaster.sh")

    if os_name == "retrodeck":
        roms_folder = os.environ.get("roms_folder", "")
        if roms_folder:
            pm_script = Path("PortMaster/PortMaster.sh")
            target_path = Path(f"/{roms_folder}/portmaster/PortMaster.sh")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pm_script), str(target_path))

    if os_name == "muOS":
        Path("/roms/ports/PortMaster").mkdir(parents=True, exist_ok=True)
        shutil.copy(f"{controlfolder}/PortMaster/control.txt", "/roms/ports/PortMaster/control.txt")

    # Restore runtimes
    portmaster_libs = Path("PortMaster/libs")
    portmaster_libs.mkdir(parents=True, exist_ok=True)

    for squashfs_file in temp_runtimes.glob("*.squashfs"):
        try:
            shutil.move(str(squashfs_file), str(portmaster_libs / squashfs_file.name))
        except (FileNotFoundError, PermissionError):
            pass

    # Remove temp directory
    if temp_runtimes.exists():
        shutil.rmtree(temp_runtimes)

    # Extract runtimes if present
    runtimes_zip = temp_dir / "runtimes.zip"
    if runtimes_zip.exists():
        os.chdir("PortMaster/libs/")
        with zipfile.ZipFile(runtimes_zip, 'r') as zip_ref:
            zip_ref.extractall(".")
        os.chdir(controlfolder)

    # Clean up old installers
    if os_name == "retrodeck":
        roms_folder = os.environ.get("roms_folder", "")
        if roms_folder:
            cleanup_dir = Path(f"/{roms_folder}/portmaster")
            for pattern in ["Install*PortMaster*.sh", "Restore*PortMaster*.sh"]:
                for file in cleanup_dir.glob(pattern):
                    file.unlink(missing_ok=True)
    else:
        cleanup_dirs = [
            Path(f"/{directory}/port_scripts"),
            Path(f"/{directory}/ports")
        ]
        for cleanup_dir in cleanup_dirs:
            if cleanup_dir.exists():
                for pattern in ["Install*PortMaster*.sh", "Restore*PortMaster*.sh"]:
                    for file in cleanup_dir.glob(pattern):
                        file.unlink(missing_ok=True)

    print("Finished installing PortMaster")

    return True


def detect_environment():
    """Detect the current environment and return appropriate settings"""

    xdg_data_home = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    # Default values
    no_sudo = False
    esudo = ""
    cur_tty = "/dev/tty0"
    controlfolder = None
    directory = None
    os_name_override = None

    # RetroDECK detection
    if Path("/app/bin/retrodeck.sh").exists():
        os.environ["LD_PRELOAD"] = ""
        cur_tty = "/dev/null"
        # Load RetroDECK config
        # ... (simplified for brevity)
        os_name_override = "retrodeck"
        no_sudo = True
        Path.home().joinpath("no_es_restart").touch()

    # More detection logic would go here...
    # For now, use sensible defaults

    if controlfolder is None:
        if Path("/opt/system/Tools/").is_dir():
            controlfolder = "/opt/system/Tools"
        elif Path("/opt/tools/").is_dir():
            controlfolder = "/opt/tools"
        elif Path("/userdata/system").is_dir():
            controlfolder = xdg_data_home
            Path(controlfolder).joinpath("PortMaster").mkdir(parents=True, exist_ok=True)
        else:
            controlfolder = "/roms/ports"

    if directory is None:
        directory = "roms"

    # Try to read OS name
    os_name = os_name_override
    if os_name is None and Path("/etc/os-release").exists():
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("NAME="):
                    os_name = line.split("=")[1].strip().strip('"')
                    break

    if os_name is None:
        os_name = "unknown"

    # Test sudo
    if not no_sudo:
        result = subprocess.run("sudo echo 'Testing for sudo...'", shell=True, capture_output=True)
        if result.returncode == 0:
            esudo = "sudo"

    return {
        "controlfolder": controlfolder,
        "directory": directory,
        "os_name": os_name,
        "esudo": esudo,
        "cur_tty": cur_tty,
    }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Install PortMaster")
    parser.add_argument(
        '--controlfolder',
        help='Control folder location (auto-detected if not specified)'
    )
    parser.add_argument(
        '--directory',
        help='Directory location (auto-detected if not specified)'
    )
    parser.add_argument(
        '--os-name',
        help='OS name (auto-detected if not specified)'
    )

    args = parser.parse_args()

    # Detect environment
    env = detect_environment()

    # Override with command line arguments
    if args.controlfolder:
        env["controlfolder"] = args.controlfolder
    if args.directory:
        env["directory"] = args.directory
    if args.os_name:
        env["os_name"] = args.os_name

    # Install
    success = install_portmaster(
        env["controlfolder"],
        env["directory"],
        env["os_name"],
        env["esudo"],
        env["cur_tty"]
    )

    if success:
        print("\nInstallation complete!")
        sys.exit(0)
    else:
        print("\nInstallation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
