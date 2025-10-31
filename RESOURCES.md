# PortMaster Resource Organization

## Overview

Resources in PortMaster are organized into different directories based on their purpose and usage context.

## Directory Structure

### `/PortMaster/resources/`
**Purpose**: Splash screens and error displays for shell launcher
- `background.png` - Background image for splash screen
- `splash.ini` - Configuration for splash screen display
- `error.ini` - Configuration for error screen display
- `do_init` - Initialization marker file

**Usage**: Used by `PortMaster.sh` and shell scripts for visual feedback during startup

### `/PortMaster/pylibs/resources/`
**Purpose**: Fonts and assets for Python GUI (pugwash)
- `DejaVuSans.ttf` - Default font for GUI
- `NotoSans.tar.xz` - Additional Noto Sans fonts (extracted on first run)
  - Includes international character support for localization

**Usage**: Used by the Python GUI application for text rendering

### `/PortMaster/utils/*/assets/`
**Purpose**: Assets for utility scripts
- `pmsplash/assets/` - PortMaster splash utility graphics
- `patcher/assets/` - Port patcher utility graphics and sounds

## Platform-Specific Configuration

Platform-specific configurations are stored as text files in `/PortMaster/`:

### Module Files (`mod_*.txt`)
Platform-specific behavior overrides:
- `mod_Batocera.txt` - Batocera OS customizations
- `mod_JELOS.txt` - JELOS customizations
- `mod_ROCKNIX.txt` - ROCKNIX customizations
- `mod_muOS.txt` - muOS customizations
- `mod_knulli.txt` - Knulli customizations
- `mod_TrimUI.txt` - TrimUI customizations
- `mod_Miyoo.txt` - Miyoo customizations
- etc.

### Library Configuration (`libgl_*.txt`)
OpenGL library configuration per platform:
- `libgl_default.txt` - Default GL library configuration
- `libgl_Batocera.txt` - Batocera GL configuration
- `libgl_JELOS.txt` - JELOS GL configuration
- etc.

### Other Configuration Files
- `control.txt` - Main control/configuration script (sourced by PortMaster.sh)
- `funcs.txt` - Shared shell functions
- `device_info.txt` - Device detection information
- `gamecontrollerdb.txt` - SDL game controller mappings
- `PortMasterDialog.txt` - Dialog functions for shell scripts

## Best Practices

1. **Shell Script Resources**: Keep splash screens, init files, and shell-sourced configs in `/PortMaster/resources/`

2. **Python GUI Resources**: Keep fonts and GUI assets in `/PortMaster/pylibs/resources/`

3. **Platform-Specific**: Keep platform config files (mod_*, libgl_*) in `/PortMaster/` root for easy sourcing by shell scripts

4. **Utility Assets**: Keep utility-specific assets in their respective `/PortMaster/utils/*/assets/` directories

## Loading Resources

### From Shell Scripts
```bash
source $controlfolder/control.txt
source "${controlfolder}/mod_${CFW_NAME}.txt"
```

### From Python
```python
from pathlib import Path

PYLIB_PATH = Path(__file__).parent / 'pylibs'
font_path = PYLIB_PATH / 'resources' / 'DejaVuSans.ttf'
```

## Notes

- Resources are split by execution context (shell vs Python) for clear separation of concerns
- Platform-specific files use a naming convention (mod_*, libgl_*) for easy identification
- Font archives (NotoSans.tar.xz) are extracted on first run to save space in repository
