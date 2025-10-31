# Repository Structure

This document describes the reorganized structure of the PortMaster GUI repository.

## Overview

The repository has been reorganized to separate concerns and follow best practices for Python/Bash development:

```
.
├── build/              # Build system and release scripts
│   ├── scripts/        # Release and build scripts
│   └── tools/          # Build utilities
├── dependencies/       # External dependencies
│   └── exlibs/         # External Python libraries
├── resources/          # Platform-specific resources
│   ├── binaries/       # Architecture-specific executables
│   │   ├── aarch64/    # ARM 64-bit binaries
│   │   ├── armhf/      # ARM 32-bit binaries
│   │   └── x86_64/     # x86 64-bit binaries
│   └── platforms/      # OS-specific configurations
│       ├── batocera/   # Batocera-specific files
│       ├── config/     # Platform configuration files (mod_*.txt, libgl_*.txt)
│       ├── knulli/     # Knulli-specific files
│       ├── miyoo/      # Miyoo-specific files
│       ├── muos/       # muOS-specific files
│       ├── retrodeck/  # RetroDECK-specific files
│       └── trimui/     # TrimUI-specific files
└── PortMaster/         # Main application code
    ├── pylibs/         # Python libraries and GUI code
    ├── pugwash         # Main GUI entry point
    └── harbourmaster   # CLI tool
```

## Directory Details

### `build/`
Contains all build-related scripts and tools:
- **`build/scripts/`**: Release scripts for different platforms
  - `do_release.sh` - Main release build script
  - `do_muos_release.sh` - muOS-specific release
  - `do_trimui_release.sh` - TrimUI-specific release
  - `do_x86_64_release.sh` - x86_64/RetroDECK release
  - `do_beta.sh`, `do_stable.sh` - Release channel scripts
  - `do_i18n.sh` - Internationalization build
- **`build/tools/`**: Build utilities
  - `pm_release.py` - Release version management
  - `pm_version.py` - Version JSON generation
  - `installer.sh` - Installation script
  - `download_runtimes.sh` - Runtime downloads
  - `makeself-header.sh` - Self-extracting installer header

### `dependencies/`
External dependencies that are bundled with the application:
- **`exlibs/`**: Python libraries that are packaged with PortMaster
  - ansimarkup, certifi, colorama, fastjsonschema, idna, loguru, qrcode, requests, urllib3, etc.

### `resources/`
Platform and architecture-specific resources:

#### `resources/binaries/`
Architecture-specific executables organized by platform:
- **`aarch64/`**: ARM 64-bit binaries (default for most handheld devices)
  - 7zzs, gptokeyb, gptokeyb2, innoextract, sdl2imgshow, sdl_resolution, xdelta3
- **`armhf/`**: ARM 32-bit binaries
- **`x86_64/`**: x86 64-bit binaries (for PC and RetroDECK)
- **Root level**: `libinterpose.*.so` libraries for each architecture

#### `resources/platforms/`
OS-specific configuration files and scripts:
- **`config/`**: Cross-platform configuration files
  - `mod_*.txt` - Platform-specific modifications
  - `libgl_*.txt` - OpenGL library configurations
- **Platform directories**: OS-specific files
  - `control.txt` - Platform control configuration
  - `PortMaster.txt` - Platform-specific launcher script
  - `gamecontrollerdb.txt` - Game controller mappings
  - Other platform-specific resources

### `PortMaster/`
Main application code:
- **`pylibs/`**: Python libraries
  - `harbourmaster/` - Core port management library
  - `default_theme/` - Default GUI theme
  - `locales/` - Internationalization files
  - GUI modules (pySDL2gui.py, pugscene.py, pugtheme.py, utility.py)
- **`pugwash`**: Main GUI application entry point - references `dependencies/exlibs/` for external libraries
- **`harbourmaster`**: CLI tool for port management - references `dependencies/exlibs/` for external libraries

The Python scripts have been updated to reference the new file locations directly:
- `EXLIB_PATH` points to `../dependencies/exlibs/`
- Build scripts copy platform config files from `resources/platforms/config/` during packaging

## Backward Compatibility

To maintain backward compatibility with existing scripts and code, symbolic links are used in the `PortMaster/` directory. This allows:
1. Existing code to continue working without modifications
2. Clean separation of concerns in the repository
3. Easy maintenance and organization

## Build Process

The build process has been updated to work with the new structure:

1. **Development**: Work with the reorganized structure, scripts reference new paths
2. **Packaging**: 
   - `build/scripts/do_release.sh` creates `pylibs.zip` from `dependencies/exlibs/` and `PortMaster/pylibs/`
   - Platform config files from `resources/platforms/config/` are copied into `PortMaster.zip` during build
3. **Distribution**: Platform-specific scripts copy appropriate resources from `resources/platforms/`

## Running Locally

For development, run from the repository root:
```bash
python3 PortMaster/pugwash
```

The Python scripts reference `dependencies/exlibs/` directly for external dependencies.

## Building Releases

From the repository root:
```bash
# Main release
./build/scripts/do_release.sh

# Platform-specific releases
./build/scripts/do_muos_release.sh [stable]
./build/scripts/do_trimui_release.sh [stable]
./build/scripts/do_x86_64_release.sh [stable|beta|alpha]
```

## Benefits of New Structure

1. **Clear Separation**: Build logic, dependencies, resources, and application code are clearly separated
2. **Maintainability**: Easier to find and modify platform-specific configurations
3. **Scalability**: Adding new platforms or architectures is straightforward
4. **Best Practices**: Follows Python/Bash project conventions
5. **Direct References**: Scripts reference files in their organized locations without indirection
