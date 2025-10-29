# Migration Guide: Repository Restructuring

This guide explains the repository restructuring changes and how to adapt to the new structure.

## What Changed?

The repository has been reorganized from an "all-in-one" structure to a well-organized, maintainable structure following best practices.

### Key Changes

1. **Build scripts moved**: `do_*.sh` scripts moved from root to `build/scripts/`
2. **Build tools moved**: `tools/` directory moved to `build/tools/`
3. **Dependencies separated**: `PortMaster/exlibs/` moved to `dependencies/exlibs/`
4. **Platform binaries organized**: Architecture-specific binaries moved to `resources/binaries/{aarch64,armhf,x86_64}/`
5. **Platform configs organized**: OS-specific files moved to `resources/platforms/`
6. **Config files organized**: mod_*.txt and libgl_*.txt moved to `resources/platforms/config/`

## For Developers

### Running the Application

**Before (still works):**
```bash
python3 PortMaster/pugwash
```

**The symlinks ensure backward compatibility** - no changes needed to your workflow!

### Building Releases

**Before:**
```bash
./do_release.sh
./do_muos_release.sh stable
```

**After:**
```bash
./build/scripts/do_release.sh
./build/scripts/do_muos_release.sh stable
```

You can also create aliases or wrapper scripts at the root if desired.

### Code Changes Required

**None!** The symlinks in `PortMaster/` mean:
- Python imports work unchanged
- Binary references work unchanged
- Platform config access works unchanged

### Understanding the New Structure

See [STRUCTURE.md](STRUCTURE.md) for a comprehensive overview of the new directory layout.

### Key Locations

| What | Old Location | New Location | Symlink |
|------|-------------|--------------|---------|
| Build scripts | `./do_*.sh` | `build/scripts/do_*.sh` | No |
| Build tools | `tools/` | `build/tools/` | No |
| External Python libs | `PortMaster/exlibs/` | `dependencies/exlibs/` | Yes |
| ARM64 binaries | `PortMaster/*.aarch64` | `resources/binaries/aarch64/` | Yes |
| ARM32 binaries | `PortMaster/*.armhf` | `resources/binaries/armhf/` | Yes |
| x86_64 binaries | `PortMaster/*.x86_64` | `resources/binaries/x86_64/` | Yes |
| Platform configs | `PortMaster/{miyoo,muos,...}/` | `resources/platforms/*/` | Yes |
| Config files | `PortMaster/mod_*.txt` | `resources/platforms/config/` | Yes |

## For Contributors

### Adding a New Platform

**Before:** Files scattered in PortMaster/
**After:** Create new directory in `resources/platforms/your_platform/` with:
- `control.txt`
- `PortMaster.txt` (launch script)
- Any platform-specific assets

Then add a symlink:
```bash
cd PortMaster
ln -s ../resources/platforms/your_platform your_platform
```

### Adding a New Architecture Binary

Place binaries in `resources/binaries/your_arch/` and create symlinks in `PortMaster/`.

### Modifying Build Scripts

Build scripts are now in `build/scripts/`. They reference:
- `build/tools/` for build utilities
- `resources/platforms/` for platform-specific files
- `dependencies/exlibs/` for external libraries (via symlink)

## Benefits

1. **Clarity**: Easy to find build scripts, platform configs, and binaries
2. **Maintainability**: Changes to platform configs don't clutter application code
3. **Scalability**: Adding new platforms/architectures is straightforward
4. **Best Practices**: Follows Python and Bash project conventions
5. **Backward Compatibility**: Symlinks preserve existing behavior

## Troubleshooting

### "Build script not found"

Update your commands to use `build/scripts/` prefix or create wrapper scripts.

### "Cannot find exlibs"

The symlink `PortMaster/exlibs` should point to `../dependencies/exlibs`. Verify with:
```bash
ls -la PortMaster/exlibs
```

### "Binary not found"

Check that symlinks in `PortMaster/` point to `resources/binaries/`. Verify with:
```bash
ls -la PortMaster/*.aarch64
```

## Questions?

See [STRUCTURE.md](STRUCTURE.md) for detailed documentation or open an issue.
