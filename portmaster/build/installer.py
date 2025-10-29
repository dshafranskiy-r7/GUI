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


def install_portmaster(controlfolder, directory, os_name, esudo="", cur_tty="/dev/tty0"):
    """Install PortMaster to the specified location"""
    
    print(f"-- Installing on {os_name} --")
    
    # Create temp directory for runtimes
    temp_dir = Path.cwd()
    os.chdir(controlfolder)
    
    print(f"Installing PortMaster to {controlfolder}")
    
    # Move existing runtimes to temp
    subprocess.run(f"{esudo} mkdir -p temp_runtimes", shell=True)
    subprocess.run(f"{esudo} mv -f PortMaster/libs/*.squashfs temp_runtimes/ 2>/dev/null || true", shell=True)
    
    # Remove old PortMaster
    subprocess.run(f"{esudo} rm -fR PortMaster PortMaster.sh", shell=True)
    
    # Handle JELOS/ROCKNIX special case
    if os_name in ["JELOS", "ROCKNIX"]:
        jelos_config = Path("/storage/.config/PortMaster")
        if not jelos_config.exists():
            subprocess.run("mkdir -p /storage/.config/ports/PortMaster", shell=True)
            subprocess.run("cp -rv /usr/config/PortMaster /storage/.config/", shell=True)
        
        os.chdir("/storage/.config/PortMaster")
        subprocess.run("cp -v /usr/config/PortMaster/PortMaster.sh PortMaster.sh", shell=True)
        subprocess.run("cp -v /usr/config/PortMaster/control.txt control.txt", shell=True)
        subprocess.run("rm -f gamecontrollerdb.txt", shell=True)
        subprocess.run("ln -svf /usr/config/SDL-GameControllerDB/gamecontrollerdb.txt gamecontrollerdb.txt", shell=True)
        subprocess.run("rm -f gptokeyb", shell=True)
        subprocess.run("ln -svf /usr/bin/gptokeyb gptokeyb", shell=True)
        subprocess.run("cp -v /usr/config/PortMaster/portmaster.gptk portmaster.gptk", shell=True)
        
        os.chdir(controlfolder)
    
    # Extract PortMaster.zip
    portmaster_zip = temp_dir / "PortMaster.zip"
    subprocess.run(f"{esudo} unzip -o {portmaster_zip}", shell=True)
    
    # Apply OS-specific overrides
    if os_name:
        portmaster_dir = Path(controlfolder) / "PortMaster"
        override_dir = portmaster_dir / os_name.lower()
        
        print(f"--> {override_dir} <--")
        if override_dir.exists():
            portmaster_txt = override_dir / "PortMaster.txt"
            control_txt = override_dir / "control.txt"
            
            if portmaster_txt.exists():
                subprocess.run(f"{esudo} cp -vf {portmaster_txt} {portmaster_dir}/PortMaster.sh", shell=True)
            if control_txt.exists():
                subprocess.run(f"{esudo} cp -vf {control_txt} {portmaster_dir}/", shell=True)
    
    # Move PortMaster.sh to appropriate location
    relocate_pm = os_name not in ["JELOS", "UnofficialOS", "ROCKNIX", "muOS", "retrodeck"]
    
    if relocate_pm:
        if Path("/userdata/roms/ports").is_dir():
            subprocess.run(f"{esudo} mv -vf PortMaster/PortMaster.sh /{directory}/ports/PortMaster.sh", shell=True)
        else:
            subprocess.run(f"{esudo} mv -vf PortMaster/PortMaster.sh PortMaster.sh", shell=True)
    
    if os_name == "retrodeck":
        roms_folder = os.environ.get("roms_folder", "")
        if roms_folder:
            subprocess.run(f"{esudo} mv -vf PortMaster/PortMaster.sh /{roms_folder}/portmaster/PortMaster.sh", shell=True)
    
    if os_name == "muOS":
        subprocess.run("mkdir -p /roms/ports/PortMaster", shell=True)
        subprocess.run(f"cp -f {controlfolder}/PortMaster/control.txt /roms/ports/PortMaster/control.txt", shell=True)
    
    # Restore runtimes
    subprocess.run(f"{esudo} mv -f temp_runtimes/*.squashfs PortMaster/libs/ 2>/dev/null || true", shell=True)
    subprocess.run(f"{esudo} rm -fR temp_runtimes/", shell=True)
    
    # Extract runtimes if present
    runtimes_zip = temp_dir / "runtimes.zip"
    if runtimes_zip.exists():
        os.chdir("PortMaster/libs/")
        subprocess.run(f"{esudo} unzip -o {runtimes_zip}", shell=True)
        os.chdir(controlfolder)
    
    # Clean up old installers
    if os_name == "retrodeck":
        roms_folder = os.environ.get("roms_folder", "")
        if roms_folder:
            subprocess.run(f"{esudo} rm -vf /{roms_folder}/portmaster/Install*PortMaster*.sh", shell=True)
            subprocess.run(f"{esudo} rm -vf /{roms_folder}/portmaster/Restore*PortMaster*.sh", shell=True)
    else:
        subprocess.run(f"{esudo} rm -vf /{directory}/port_scripts/Install*PortMaster*.sh", shell=True)
        subprocess.run(f"{esudo} rm -vf /{directory}/port_scripts/Restore*PortMaster*.sh", shell=True)
        subprocess.run(f"{esudo} rm -vf /{directory}/ports/Install*PortMaster*.sh", shell=True)
        subprocess.run(f"{esudo} rm -vf /{directory}/ports/Restore*PortMaster*.sh", shell=True)
    
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
