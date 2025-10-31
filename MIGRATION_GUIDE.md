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

**No changes needed:**
```bash
python3 PortMaster/pugwash
```

The Python scripts have been updated to reference `dependencies/exlibs/` directly.

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

**Minimal changes:**
- Python scripts (`pugwash`, `harbourmaster`) now reference `dependencies/exlibs/` directly
- Build scripts copy platform config files during packaging
- No changes to application logic or behavior

### Understanding the New Structure

See [STRUCTURE.md](STRUCTURE.md) for a comprehensive overview of the new directory layout.

### Key Locations

| What | Old Location | New Location | Access Method |
|------|-------------|--------------|---------------|
| Build scripts | `./do_*.sh` | `build/scripts/do_*.sh` | Direct path |
| Build tools | `tools/` | `build/tools/` | Direct path |
| External Python libs | `PortMaster/exlibs/` | `dependencies/exlibs/` | Python path reference |
| ARM64 binaries | `PortMaster/*.aarch64` | `resources/binaries/aarch64/` | Copied during build |
| ARM32 binaries | `PortMaster/*.armhf` | `resources/binaries/armhf/` | Copied during build |
| x86_64 binaries | `PortMaster/*.x86_64` | `resources/binaries/x86_64/` | Copied during build |
| Platform configs | `PortMaster/{miyoo,muos,...}/` | `resources/platforms/*/` | Copied during build |
| Config files | `PortMaster/mod_*.txt` | `resources/platforms/config/` | Copied during build |

## For Contributors

### Adding a New Platform

**Before:** Files scattered in PortMaster/
**After:** Create new directory in `resources/platforms/your_platform/` with:
- `control.txt`
- `PortMaster.txt` (launch script)
- Any platform-specific assets

Platform-specific build scripts will reference these files directly.

### Adding a New Architecture Binary

Place binaries in `resources/binaries/your_arch/`. Build scripts will package them as needed.

### Modifying Build Scripts

Build scripts are now in `build/scripts/`. They reference:
- `build/tools/` for build utilities
- `resources/platforms/` for platform-specific files
- `dependencies/exlibs/` for external libraries

## Benefits

1. **Clarity**: Easy to find build scripts, platform configs, and binaries
2. **Maintainability**: Changes to platform configs don't clutter application code
3. **Scalability**: Adding new platforms/architectures is straightforward
4. **Best Practices**: Follows Python and Bash project conventions
5. **Direct References**: No symlink indirection - scripts reference actual file locations

## Troubleshooting

### "Build script not found"

Update your commands to use `build/scripts/` prefix.

### "Cannot find exlibs"

The Python scripts now reference `dependencies/exlibs` directly. If you get import errors, ensure the `dependencies/exlibs` directory exists.

### "Config files missing at runtime"

Config files are copied into `PortMaster.zip` during the build process. If running from source, they're in `resources/platforms/config/`.

## Questions?

See [STRUCTURE.md](STRUCTURE.md) for detailed documentation or open an issue.
