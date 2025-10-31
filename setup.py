#!/usr/bin/env python3
"""
Setup script for PortMaster GUI
Provides custom build commands to replace bash scripts
"""

import os
import sys
import shutil
import subprocess
import datetime
import hashlib
import json
import zipfile
from pathlib import Path
from setuptools import setup, Command
from setuptools.command.build import build as _build


class CompileI18nCommand(Command):
    """Custom command to compile translation files (replaces do_i18n.sh)"""
    
    description = "Compile translation (.po) files to binary (.mo) format"
    user_options = [
        ('download', 'd', 'Download translations from Crowdin before compiling'),
    ]
    
    def initialize_options(self):
        self.download = False
    
    def finalize_options(self):
        pass
    
    def run(self):
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
                    print(f"  Compiling {pot_file}.po to {pot_file}.mo")
                    result = subprocess.run(
                        ["msgfmt", "-v", "-o", str(lang_mo_file), str(lang_po_file)],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        print(f"  Warning: Failed to compile {lang_po_file}")
                        print(result.stderr)


class ExtractI18nCommand(Command):
    """Custom command to extract translatable strings (part of do_i18n.sh)"""
    
    description = "Extract translatable strings from source files"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Extract strings for translation"""
        pot_dir = Path("PortMaster/pylibs/locales")
        pot_files = {
            "messages": [
                "PortMaster/pugwash",
                "PortMaster/pylibs/harbourmaster/*.py",
                "PortMaster/pylibs/pug*.py"
            ],
        }
        
        print("Extracting translatable strings...")
        
        for pot_file, sources in pot_files.items():
            pot_path = pot_dir / f"{pot_file}.pot"
            print(f"Extracting {pot_file}.pot from {len(sources)} source patterns")
            
            # Build file list
            files = []
            for pattern in sources:
                if '*' in pattern:
                    base_dir = pattern.rsplit('/', 1)[0]
                    glob_pattern = pattern.rsplit('/', 1)[1]
                    files.extend([str(f) for f in Path(base_dir).glob(glob_pattern)])
                else:
                    files.append(pattern)
            
            # Run xgettext
            result = subprocess.run(
                ["xgettext", "-v", "-o", str(pot_path), "-L", "Python"] + files,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Warning: Failed to extract strings for {pot_file}")
                print(result.stderr)


class BuildPylibsCommand(Command):
    """Custom command to build pylibs.zip"""
    
    description = "Build pylibs.zip archive"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Create pylibs.zip"""
        print("Creating pylibs.zip...")
        
        os.chdir("PortMaster")
        
        # Remove old pylibs.zip
        if Path("pylibs.zip").exists():
            Path("pylibs.zip").unlink()
        
        # Create new pylibs.zip
        with zipfile.ZipFile("pylibs.zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for root, dirs, files in os.walk("exlibs"):
                # Skip __pycache__ and .DS_Store
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for file in files:
                    if file == ".DS_Store" or file.startswith("._") or "NotoSans" in file:
                        continue
                    file_path = Path(root) / file
                    zf.write(file_path, file_path)
            
            for root, dirs, files in os.walk("pylibs"):
                # Skip __pycache__ and .DS_Store
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for file in files:
                    if file == ".DS_Store" or file.startswith("._") or "NotoSans" in file:
                        continue
                    file_path = Path(root) / file
                    zf.write(file_path, file_path)
        
        os.chdir("..")
        print(f"Created pylibs.zip ({Path('PortMaster/pylibs.zip').stat().st_size} bytes)")


class SetVersionCommand(Command):
    """Custom command to set version (replaces tools/pm_release.py)"""
    
    description = "Set version and release channel"
    user_options = [
        ('release-type=', 'r', 'Release type (alpha/beta/stable)'),
        ('version-number=', 'v', 'Version number (defaults to current timestamp)'),
    ]
    
    def initialize_options(self):
        self.release_type = 'alpha'
        self.version_number = None
    
    def finalize_options(self):
        if self.version_number is None:
            self.version_number = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d-%H%M")
    
    def run(self):
        """Update version in pugwash file"""
        print(f"Setting version to {self.version_number} ({self.release_type})")
        
        pugwash_file = Path("PortMaster/pugwash")
        
        # Read file
        with open(pugwash_file, 'r') as f:
            lines = f.readlines()
        
        # Update version
        for i, line in enumerate(lines):
            if line.startswith("PORTMASTER_VERSION ="):
                lines[i] = f"PORTMASTER_VERSION = '{self.version_number}'\n"
                print(f"Updated PORTMASTER_VERSION to {self.version_number}")
            elif line.startswith("PORTMASTER_RELEASE_CHANNEL ="):
                lines[i] = f"PORTMASTER_RELEASE_CHANNEL = '{self.release_type}'\n"
                print(f"Updated PORTMASTER_RELEASE_CHANNEL to {self.release_type}")
        
        # Write file
        with open(pugwash_file, 'w') as f:
            f.writelines(lines)
        
        # Create version file
        with open("PortMaster/version", 'w') as f:
            f.write(self.version_number)
        
        with open("version", 'w') as f:
            f.write(self.version_number)


class BuildReleaseCommand(Command):
    """Custom command to build release (replaces do_release.sh)"""
    
    description = "Build PortMaster.zip release package"
    user_options = [
        ('release-type=', 'r', 'Release type (alpha/beta/stable)'),
        ('make-install', 'i', 'Create installer packages'),
    ]
    
    def initialize_options(self):
        self.release_type = 'alpha'
        self.make_install = False
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Build PortMaster.zip"""
        print(f"Building release ({self.release_type})...")
        
        # Set version first
        self.run_command('set_version')
        
        # Compile translations
        self.run_command('compile_i18n')
        
        # Build pylibs.zip
        self.run_command('build_pylibs')
        
        # Clean up .DS_Store and other temp files
        print("Cleaning up temporary files...")
        for root, dirs, files in os.walk("."):
            for file in files:
                if file == ".DS_Store" or file.startswith("._"):
                    file_path = Path(root) / file
                    file_path.unlink()
                    print(f"Removed {file_path}")
        
        # Remove old PortMaster.zip
        if Path("PortMaster.zip").exists():
            Path("PortMaster.zip").unlink()
        
        # Create PortMaster.zip
        print("Creating PortMaster.zip...")
        excludes = [
            "PortMaster/pylibs/",
            "PortMaster/exlibs/",
            "PortMaster/config/",
            "PortMaster/themes/",
            "PortMaster/libs/*.squashfs",
            "PortMaster/libs/*.squashfs.md5",
            "PortMaster/pugwash.bak",
            "PortMaster/log.txt",
            "PortMaster/pugwash.txt",
            "PortMaster/harbourmaster.txt",
        ]
        
        with zipfile.ZipFile("PortMaster.zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for root, dirs, files in os.walk("PortMaster"):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if not any(
                    Path(root).joinpath(d).match(excl.rstrip('/')) 
                    for excl in excludes
                )]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip excluded files
                    if any(file_path.match(excl) for excl in excludes):
                        continue
                    if file == ".DS_Store" or file.startswith("._"):
                        continue
                    
                    zf.write(file_path, file_path)
        
        print(f"Created PortMaster.zip ({Path('PortMaster.zip').stat().st_size} bytes)")
        
        if self.make_install:
            print("Note: Installer creation requires makeself and will be handled separately")


class CustomBuildCommand(_build):
    """Custom build command that includes our custom steps"""
    
    def run(self):
        # Compile translations
        self.run_command('compile_i18n')
        # Run standard build
        _build.run(self)


# Run setup
if __name__ == "__main__":
    setup(
        cmdclass={
            'build': CustomBuildCommand,
            'compile_i18n': CompileI18nCommand,
            'extract_i18n': ExtractI18nCommand,
            'build_pylibs': BuildPylibsCommand,
            'set_version': SetVersionCommand,
            'build_release': BuildReleaseCommand,
        },
    )
