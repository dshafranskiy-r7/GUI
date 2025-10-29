#!/usr/bin/env python3
"""
Release building module for PortMaster
Replaces the do_release.sh script
"""

import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def hash_file(file_name):
    """Calculate MD5 hash of a file"""
    md5_obj = hashlib.md5()
    
    with open(file_name, 'rb') as fh:
        for data in iter(lambda: fh.read(4096), b''):
            md5_obj.update(data)
    
    return md5_obj.hexdigest()


def update_version(release_type='alpha', version_number=None):
    """Update version in pugwash file"""
    if version_number is None:
        version_number = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H%M")
    
    print(f"Setting version to {version_number} ({release_type})")
    
    pugwash_file = Path("PortMaster/pugwash")
    
    # Backup
    shutil.copy(pugwash_file, str(pugwash_file) + ".bak")
    
    # Read file
    with open(pugwash_file, 'r') as f:
        lines = f.readlines()
    
    # Update version
    for i, line in enumerate(lines):
        if line.startswith("PORTMASTER_VERSION ="):
            lines[i] = f"PORTMASTER_VERSION = '{version_number}'\n"
        elif line.startswith("PORTMASTER_RELEASE_CHANNEL ="):
            lines[i] = f"PORTMASTER_RELEASE_CHANNEL = '{release_type}'\n"
    
    # Write file
    with open(pugwash_file, 'w') as f:
        f.writelines(lines)
    
    # Create version file
    with open("PortMaster/version", 'w') as f:
        f.write(version_number)
    
    with open("version", 'w') as f:
        f.write(version_number)
    
    return version_number


def compile_translations():
    """Compile .po files to .mo files"""
    pot_dir = Path("PortMaster/pylibs/locales")
    pot_files = ["messages", "themes"]
    
    print("Compiling translation files...")
    
    for lang_dir in pot_dir.iterdir():
        if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
            continue
            
        lang_code = lang_dir.name
        print(f"Processing {lang_code}:")
        
        for pot_file in pot_files:
            lang_pot_file = lang_dir / "LC_MESSAGES" / f"{pot_file}.pot"
            lang_po_file = lang_dir / "LC_MESSAGES" / f"{pot_file}.po"
            lang_mo_file = lang_dir / "LC_MESSAGES" / f"{pot_file}.mo"
            
            # Rename .pot to .po if needed
            if lang_pot_file.exists():
                shutil.move(str(lang_pot_file), str(lang_po_file))
            
            # Compile .po to .mo
            if lang_po_file.exists():
                print(f"  Compiling {pot_file}.po")
                result = subprocess.run(
                    ["msgfmt", "-v", "-o", str(lang_mo_file), str(lang_po_file)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"  Warning: Failed to compile {lang_po_file}")


def build_pylibs_zip():
    """Create pylibs.zip"""
    print("Creating pylibs.zip...")
    
    os.chdir("PortMaster")
    
    # Remove old pylibs.zip
    if Path("pylibs.zip").exists():
        Path("pylibs.zip").unlink()
    
    # Create new pylibs.zip using subprocess (to match original behavior)
    cmd = [
        "zip", "-9r", "pylibs.zip", "exlibs/", "pylibs/",
        "-x", "*__pycache__*/*",
        "-x", "*.DS_Store",
        "-x", "._*",
        "-x", "*NotoSans*.ttf"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Warning: zip command failed: {result.stderr}")
    
    os.chdir("..")
    
    size = Path("PortMaster/pylibs.zip").stat().st_size
    print(f"Created pylibs.zip ({size} bytes)")


def build_portmaster_zip():
    """Create PortMaster.zip"""
    print("Creating PortMaster.zip...")
    
    # Remove old PortMaster.zip
    if Path("PortMaster.zip").exists():
        Path("PortMaster.zip").unlink()
    
    # Create PortMaster.zip using subprocess (to match original behavior)
    cmd = [
        "zip", "-9r", "PortMaster.zip", "PortMaster/",
        "-x", "PortMaster/pylibs/*",
        "-x", "PortMaster/exlibs/*",
        "-x", "PortMaster/config/*",
        "-x", "PortMaster/themes/*",
        "-x", "PortMaster/libs/*.squashfs",
        "-x", "PortMaster/libs/*.squashfs.md5",
        "-x", "PortMaster/pugwash.bak",
        "-x", "PortMaster/log.txt",
        "-x", "PortMaster/pugwash.txt",
        "-x", "PortMaster/harbourmaster.txt",
        "-x", "*.DS_Store"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Warning: zip command failed: {result.stderr}")
    
    size = Path("PortMaster.zip").stat().st_size
    print(f"Created PortMaster.zip ({size} bytes)")


def update_version_json(release_type, version_number):
    """Update version.json with release information"""
    updates = {
        "stable": ("stable", "beta", "alpha"),
        "beta": ("beta", "alpha"),
        "alpha": ("alpha",),
    }
    
    download_url = "https://github.com/PortsMaster/PortMaster-GUI/releases/download"
    
    # Download version.json if it doesn't exist
    if not Path("version.json").exists():
        print("Downloading version.json...")
        result = subprocess.run(
            ["wget", "https://github.com/PortsMaster/PortMaster-GUI/releases/latest/download/version.json"],
            capture_output=True
        )
        if result.returncode != 0:
            print("Warning: Could not download version.json")
            return
    
    md5sum = hash_file("PortMaster.zip")
    
    with open("version.json", "r") as fh:
        version_data = json.load(fh)
    
    for update in updates.get(release_type, [release_type]):
        if update not in version_data:
            version_data[update] = {}
        version_data[update]['md5'] = md5sum
        version_data[update]['version'] = version_number
        version_data[update]['url'] = f"{download_url}/{version_number}/PortMaster.zip"
    
    with open("version.json", "w") as fh:
        json.dump(version_data, fh, indent=4)
    
    print(f"Updated version.json for {release_type} release")


def cleanup_temp_files():
    """Clean up .DS_Store and other temporary files"""
    print("Cleaning up temporary files...")
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == ".DS_Store" or file.startswith("._"):
                file_path = Path(root) / file
                try:
                    file_path.unlink()
                except Exception as e:
                    print(f"Warning: Could not remove {file_path}: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Build PortMaster release")
    parser.add_argument(
        'release_type',
        nargs='?',
        default='alpha',
        choices=['alpha', 'beta', 'stable'],
        help='Release type (default: alpha)'
    )
    parser.add_argument(
        'version_number',
        nargs='?',
        help='Version number (default: current timestamp)'
    )
    parser.add_argument(
        '--make-install',
        action='store_true',
        help='Create installer packages'
    )
    
    args = parser.parse_args()
    
    # Update version
    version_number = update_version(args.release_type, args.version_number)
    
    # Compile translations
    compile_translations()
    
    # Build pylibs.zip
    build_pylibs_zip()
    
    # Clean up temp files
    cleanup_temp_files()
    
    # Build PortMaster.zip
    build_portmaster_zip()
    
    # Update version.json
    update_version_json(args.release_type, version_number)
    
    # Restore backup
    if Path("PortMaster/pugwash.bak").exists():
        shutil.move("PortMaster/pugwash.bak", "PortMaster/pugwash")
    
    if args.make_install:
        print("\nNote: Installer creation requires makeself and is not yet implemented")
        print("Run the original do_release.sh with 'stable' argument to create installers")
    
    print("\nRelease build complete!")


if __name__ == "__main__":
    main()
