# PortMaster Build System

This directory contains Python modules that replace the bash installer/bundler scripts with a setuptools-based build system.

## Modules

### release.py
Replaces `do_release.sh` - Builds PortMaster releases

**Usage:**
```bash
python3 -m portmaster.build.release [alpha|beta|stable] [version_number]
python3 -m portmaster.build.release stable --make-install
```

### i18n.py
Replaces `do_i18n.sh` - Manages internationalization (translations)

**Usage:**
```bash
python3 -m portmaster.build.i18n [extract|upload|download|compile|full]
```

Actions:
- `extract`: Extract translatable strings from source files
- `upload`: Upload translations to Crowdin
- `download`: Download translations from Crowdin
- `compile`: Compile .po files to .mo files
- `full`: Complete workflow (extract, upload, download, compile)

### installer.py
Replaces `tools/installer.sh` - Installs PortMaster on target systems

**Usage:**
```bash
python3 -m portmaster.build.installer [options]
```

### runtimes.py
Replaces `tools/download_runtimes.sh` - Downloads runtime files

**Usage:**
```bash
python3 -m portmaster.build.runtimes --arch [aarch64|x86_64|armhf] [--output-dir DIR]
```

## Setuptools Integration

The build system is integrated with setuptools via `setup.py` and `pyproject.toml`.

### Custom Commands

Available via `python3 setup.py`:

- `python3 setup.py compile_i18n` - Compile translations
- `python3 setup.py extract_i18n` - Extract translatable strings
- `python3 setup.py build_pylibs` - Build pylibs.zip
- `python3 setup.py set_version --release-type=beta` - Set version
- `python3 setup.py build_release --release-type=stable` - Build release

### Console Scripts

After installation (`pip install -e .`), these commands are available:

- `portmaster-gui` - Run the PortMaster GUI
- `portmaster-release` - Build releases
- `portmaster-i18n` - Manage translations
- `portmaster-installer` - Install PortMaster
- `portmaster-runtimes` - Download runtimes

## Backward Compatibility

The original bash scripts (`do_release.sh`, `do_i18n.sh`, etc.) have been replaced with thin wrapper scripts that call the Python modules. The original scripts are preserved as `.original` files.

This ensures existing workflows continue to work while benefiting from the Python implementation.

## Advantages

1. **Cross-platform**: Python is more portable than bash
2. **Maintainable**: Python code is easier to read and maintain than complex bash scripts
3. **Testable**: Python modules can be unit tested
4. **Extensible**: Easy to add new features and commands
5. **Consistent**: Single source of truth via setuptools
6. **Dependencies**: Explicit dependency management via pyproject.toml
