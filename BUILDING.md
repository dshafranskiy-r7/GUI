# Building PortMaster

PortMaster now uses a Python setuptools-based build system instead of bash scripts. This provides better cross-platform support, maintainability, and testability.

## Quick Start

### Using the Python Modules Directly

Build a release:
```bash
python3 -m portmaster.build.release alpha
python3 -m portmaster.build.release beta
python3 -m portmaster.build.release stable --make-install
```

Manage translations:
```bash
python3 -m portmaster.build.i18n compile
python3 -m portmaster.build.i18n full
```

Download runtimes:
```bash
python3 -m portmaster.build.runtimes --arch aarch64
python3 -m portmaster.build.runtimes --arch x86_64
```

### Using Setuptools Commands

```bash
python3 setup.py compile_i18n
python3 setup.py build_pylibs
python3 setup.py build_release --release-type=stable
```

### Using Console Scripts (After Installation)

Install in development mode:
```bash
pip install -e .
```

Then use the installed commands:
```bash
portmaster-release stable
portmaster-i18n compile
portmaster-runtimes --arch aarch64
```

## Backward Compatibility

For users of the old bash scripts, wrapper scripts have been provided:

```bash
./do_release.sh stable
./do_i18n.sh
./do_beta.sh
./do_stable.sh
```

These wrappers call the new Python modules internally.

## Requirements

### Core Requirements
- Python 3.9 or newer
- setuptools 68.0 or newer

### Optional Requirements
- `msgfmt` (from gettext) - For compiling translations
- `xgettext` (from gettext) - For extracting translatable strings
- `crowdin` CLI - For uploading/downloading translations
- `zip` command - For creating archives
- `wget` or `curl` - For downloading files

## Build Process

The build process is now handled by Python modules in `portmaster/build/`:

1. **release.py** - Main release building
   - Updates version in pugwash file
   - Compiles translations
   - Builds pylibs.zip
   - Creates PortMaster.zip
   - Updates version.json

2. **i18n.py** - Translation management
   - Extracts translatable strings
   - Uploads/downloads from Crowdin
   - Compiles .po to .mo files

3. **installer.py** - Installation on target devices
   - Detects device environment
   - Installs PortMaster files
   - Handles platform-specific configurations

4. **runtimes.py** - Runtime downloads
   - Downloads runtime files from GitHub
   - Verifies MD5 checksums
   - Supports multiple architectures

## Development

### Project Structure

```
GUI/
├── portmaster/               # Python package
│   ├── __init__.py
│   ├── main.py              # GUI entry point
│   └── build/               # Build system modules
│       ├── __init__.py
│       ├── release.py       # Release building
│       ├── i18n.py          # Translation management
│       ├── installer.py     # Installation
│       ├── runtimes.py      # Runtime downloads
│       └── README.md        # Build system docs
├── PortMaster/              # Application files
│   ├── pugwash             # Main GUI script
│   ├── pylibs/             # Python libraries
│   └── exlibs/             # External libraries
├── pyproject.toml          # Project metadata
├── setup.py                # Setuptools configuration
├── requirements.txt        # Python dependencies
└── do_release.sh           # Wrapper script (calls Python)
```

### Adding New Build Commands

To add a new build command:

1. Create a new module in `portmaster/build/`
2. Add a `main()` function
3. Register it in `pyproject.toml` under `[project.scripts]`
4. Optionally add a setuptools command class in `setup.py`

Example:
```python
# portmaster/build/mycommand.py
def main():
    """My custom build command"""
    print("Running custom command")

if __name__ == "__main__":
    main()
```

Then in `pyproject.toml`:
```toml
[project.scripts]
portmaster-mycommand = "portmaster.build.mycommand:main"
```

## Migration from Bash Scripts

The following bash scripts have been replaced:

| Old Script | New Module | Wrapper |
|-----------|------------|---------|
| `do_release.sh` | `portmaster.build.release` | Yes |
| `do_i18n.sh` | `portmaster.build.i18n` | Yes |
| `do_beta.sh` | Wrapper to `release` | Yes |
| `do_stable.sh` | Wrapper to `release` | Yes |
| `tools/installer.sh` | `portmaster.build.installer` | Yes |
| `tools/download_runtimes.sh` | `portmaster.build.runtimes` | Yes |

Original bash scripts are preserved as `.original` files for reference.

## Testing

To test the build system:

```bash
# Test module imports
python3 -m py_compile portmaster/*.py portmaster/build/*.py

# Test help commands
python3 -m portmaster.build.release --help
python3 -m portmaster.build.i18n --help
python3 -m portmaster.build.runtimes --help

# Test wrapper scripts
./do_release.sh alpha
```

## Advantages

1. **Cross-platform**: Works on Linux, macOS, and Windows
2. **Maintainable**: Python is easier to read and maintain than bash
3. **Testable**: Modules can be unit tested
4. **Extensible**: Easy to add new features
5. **Consistent**: Single source of truth via setuptools
6. **Dependencies**: Explicit dependency management
7. **Installable**: Can be installed as a Python package

## Troubleshooting

### Import Errors

If you see import errors, ensure you're in the project root:
```bash
cd /path/to/GUI
python3 -m portmaster.build.release
```

### Missing Dependencies

Install required tools:
```bash
# On Ubuntu/Debian
sudo apt-get install gettext zip wget

# On macOS
brew install gettext
```

### Permission Errors

Ensure scripts are executable:
```bash
chmod +x do_release.sh do_i18n.sh
```

## See Also

- `portmaster/build/README.md` - Detailed build system documentation
- `BUILDING_STUFF.md` - Building native components
- `DEVELOPING.md` - Development guidelines
