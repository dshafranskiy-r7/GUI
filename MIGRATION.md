# Migration Guide: Bash Scripts to Setuptools

This guide explains the changes from bash-based build scripts to the new Python setuptools system.

## What Changed?

PortMaster's build and release process has been migrated from bash scripts to Python modules using setuptools. This provides:

- Better cross-platform support (Windows, macOS, Linux)
- Easier maintenance and testing
- More consistent behavior
- Explicit dependency management

## For End Users

**Nothing changes!** The installer and release packages work exactly the same way. You don't need to do anything.

## For Developers

### If You Used Bash Scripts

**Good news:** All bash scripts still work! They now call Python modules internally.

Your existing workflows continue to work:

```bash
./do_release.sh stable        # Still works!
./do_i18n.sh                  # Still works!
./do_beta.sh                  # Still works!
```

### New Python-Based Workflow

You can now use Python modules directly:

**Old:**
```bash
./do_release.sh stable
```

**New (equivalent):**
```bash
python3 -m portmaster.build.release stable
```

**Old:**
```bash
./do_i18n.sh
```

**New (equivalent):**
```bash
python3 -m portmaster.build.i18n full
```

### Using Setuptools Commands

You can also use setuptools commands:

```bash
python3 setup.py compile_i18n
python3 setup.py build_pylibs
python3 setup.py build_release --release-type=stable
```

### Installing as a Package

For convenience, you can install PortMaster in development mode:

```bash
pip install -e .
```

Then use console commands:

```bash
portmaster-release stable
portmaster-i18n compile
portmaster-runtimes --arch aarch64
```

## Complete Mapping

| Old Script | New Module | Wrapper Available |
|-----------|------------|-------------------|
| `./do_release.sh [type]` | `python3 -m portmaster.build.release [type]` | Yes |
| `./do_i18n.sh` | `python3 -m portmaster.build.i18n full` | Yes |
| `./do_beta.sh` | `python3 -m portmaster.build.release beta` | Yes |
| `./do_stable.sh` | `python3 -m portmaster.build.release stable` | Yes |
| `tools/installer.sh` | `python3 -m portmaster.build.installer` | Yes |
| `tools/download_runtimes.sh` | `python3 -m portmaster.build.runtimes` | Yes |

## Advanced Features

The Python modules provide additional features:

### Release Building

```bash
# Build with custom version
python3 -m portmaster.build.release stable 2023-12-01-1200

# Create installer packages
python3 -m portmaster.build.release stable --make-install
```

### Translation Management

```bash
# Just compile translations
python3 -m portmaster.build.i18n compile

# Extract strings only
python3 -m portmaster.build.i18n extract

# Upload to Crowdin
python3 -m portmaster.build.i18n upload

# Download from Crowdin
python3 -m portmaster.build.i18n download

# Complete workflow
python3 -m portmaster.build.i18n full
```

### Runtime Downloads

```bash
# Download for specific architecture
python3 -m portmaster.build.runtimes --arch aarch64
python3 -m portmaster.build.runtimes --arch x86_64
python3 -m portmaster.build.runtimes --arch armhf

# Download to specific directory
python3 -m portmaster.build.runtimes --arch aarch64 --output-dir /tmp/runtimes
```

## Troubleshooting

### "Module not found" errors

Make sure you're in the project root directory:

```bash
cd /path/to/GUI
python3 -m portmaster.build.release
```

### Import errors

Ensure Python 3.9+ is installed:

```bash
python3 --version
```

### Permission errors

Ensure scripts are executable:

```bash
chmod +x do_release.sh do_i18n.sh do_beta.sh do_stable.sh
```

## Contributing

If you're contributing to the build system:

1. Python modules are in `portmaster/build/`
2. Each module has a `main()` function
3. Modules are registered in `pyproject.toml`
4. Setuptools commands are in `setup.py`

See [BUILDING.md](BUILDING.md) for detailed developer documentation.

## FAQ

**Q: Do I need to change my CI/CD scripts?**

A: No! The bash wrapper scripts work exactly as before.

**Q: Can I still use the old bash scripts?**

A: Yes! They're preserved as `.original` files and the new wrappers call Python internally.

**Q: What if I encounter bugs?**

A: Report them on GitHub Issues. Include the command you ran and any error messages.

**Q: Why make this change?**

A: Python is more portable, testable, and maintainable than bash scripts. This will make PortMaster easier to develop and contribute to.

**Q: Will this affect the release size?**

A: No, the release packages remain the same size and structure.

## Need Help?

- See [BUILDING.md](BUILDING.md) for complete build documentation
- See [portmaster/build/README.md](portmaster/build/README.md) for build system internals
- Join the [PortMaster Discord](https://discord.gg/SbVcUM4qFp) for support
