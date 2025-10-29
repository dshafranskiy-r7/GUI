#!/usr/bin/env python3
"""
Internationalization module for PortMaster
Replaces the do_i18n.sh script
"""

import argparse
import subprocess
import sys
from pathlib import Path


def extract_strings():
    """Extract translatable strings from source files"""
    pot_dir = Path("PortMaster/pylibs/locales")
    pot_files = {
        "messages": {
            "sources": [
                "PortMaster/pugwash",
            ],
            "glob_sources": [
                ("PortMaster/pylibs/harbourmaster", "*.py"),
                ("PortMaster/pylibs", "pug*.py"),
            ]
        },
    }
    
    print("Extracting translatable strings...")
    
    for pot_file, config in pot_files.items():
        pot_path = pot_dir / f"{pot_file}.pot"
        
        # Build file list
        files = list(config["sources"])
        for base_dir, pattern in config.get("glob_sources", []):
            files.extend([str(f) for f in Path(base_dir).glob(pattern)])
        
        print(f"Extracting {pot_file}.pot from {len(files)} files")
        
        # Run xgettext
        cmd = ["xgettext", "-v", "-o", str(pot_path), "-L", "Python"] + files
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Warning: Failed to extract strings for {pot_file}")
            print(result.stderr)
        else:
            print(f"Created {pot_path}")


def extract_theme_strings():
    """Extract theme strings (themes.pot)"""
    print("Extracting theme strings...")
    
    # Run the existing theme_msgfmt.py
    result = subprocess.run(
        ["python3", "theme_msgfmt.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Warning: Failed to extract theme strings")
        print(result.stderr)
    else:
        print("Theme strings extracted")


def upload_to_crowdin():
    """Upload translations to Crowdin"""
    print("Uploading translations to Crowdin...")
    
    result = subprocess.run(["crowdin", "upload"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Warning: Failed to upload to Crowdin")
        print(result.stderr)
    else:
        print("Uploaded to Crowdin")


def download_from_crowdin():
    """Download translations from Crowdin"""
    print("Downloading translations from Crowdin...")
    
    result = subprocess.run(["crowdin", "download"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Warning: Failed to download from Crowdin")
        print(result.stderr)
    else:
        print("Downloaded from Crowdin")


def distribute_pot_files():
    """Distribute .pot files to language directories"""
    pot_dir = Path("PortMaster/pylibs/locales")
    pot_files = ["messages", "themes"]
    
    print("Distributing .pot files to language directories...")
    
    for lang_dir in pot_dir.iterdir():
        if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
            continue
        
        for pot_file in pot_files:
            source_pot = pot_dir / f"{pot_file}.pot"
            dest_po = lang_dir / "LC_MESSAGES" / f"{pot_file}.pot"
            
            if source_pot.exists():
                dest_po.parent.mkdir(parents=True, exist_ok=True)
                import shutil
                shutil.copy(source_pot, dest_po)
                print(f"Copied {pot_file}.pot to {lang_dir.name}/LC_MESSAGES/")


def compile_translations():
    """Compile .po/.pot files to .mo files"""
    pot_dir = Path("PortMaster/pylibs/locales")
    pot_files = ["messages", "themes"]
    not_working = ["da_DK", "fi_FI", "ro_RO"]
    
    print("Compiling translation files...")
    
    # Remove broken translations
    for broken in not_working:
        broken_dir = pot_dir / broken
        if broken_dir.exists():
            import shutil
            shutil.rmtree(broken_dir)
            print(f"Removed broken translation: {broken}")
    
    for lang_dir in pot_dir.iterdir():
        if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
            continue
            
        lang_code = lang_dir.name
        print(f"{lang_code}:")
        
        for pot_file in pot_files:
            lang_pot_file = lang_dir / "LC_MESSAGES" / f"{pot_file}.pot"
            lang_po_file = lang_dir / "LC_MESSAGES" / f"{pot_file}.po"
            lang_mo_file = lang_dir / "LC_MESSAGES" / f"{pot_file}.mo"
            
            # Rename .pot to .po if needed
            if lang_pot_file.exists():
                import shutil
                shutil.move(str(lang_pot_file), str(lang_po_file))
                print(f"  Renamed {pot_file}.pot to {pot_file}.po")
            
            # Compile .po to .mo
            if lang_po_file.exists():
                result = subprocess.run(
                    ["msgfmt", "-v", "-o", str(lang_mo_file), str(lang_po_file)],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"  msgfmt: {pot_file}.po -> {pot_file}.mo")
                else:
                    print(f"  Warning: Failed to compile {lang_po_file}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Manage PortMaster translations")
    parser.add_argument(
        'action',
        nargs='?',
        default='compile',
        choices=['extract', 'upload', 'download', 'compile', 'full'],
        help='Action to perform (default: compile)'
    )
    
    args = parser.parse_args()
    
    if args.action == 'extract':
        extract_strings()
        extract_theme_strings()
    
    elif args.action == 'upload':
        extract_strings()
        extract_theme_strings()
        distribute_pot_files()
        upload_to_crowdin()
    
    elif args.action == 'download':
        download_from_crowdin()
        compile_translations()
    
    elif args.action == 'compile':
        compile_translations()
    
    elif args.action == 'full':
        # Full workflow like do_i18n.sh
        extract_strings()
        extract_theme_strings()
        distribute_pot_files()
        upload_to_crowdin()
        download_from_crowdin()
        compile_translations()
    
    print("\nI18n operation complete!")


if __name__ == "__main__":
    main()
