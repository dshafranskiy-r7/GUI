# PortMaster Directory Structure

This document describes the organization of the PortMaster directory after the cleanup reorganization.

## Directory Layout

```
PortMaster/
├── archs/                      # Architecture-specific binaries
│   ├── aarch64/                # ARM 64-bit binaries
│   │   ├── 7zzs.aarch64
│   │   ├── gptokeyb
│   │   ├── gptokeyb2
│   │   ├── innoextract.aarch64
│   │   ├── libinterpose.aarch64.so
│   │   ├── sdl2imgshow.aarch64
│   │   ├── sdl_resolution.aarch64
│   │   └── xdelta3
│   ├── armhf/                  # ARM 32-bit hard float binaries
│   │   ├── 7zzs.armhf
│   │   ├── gptokeyb.armhf
│   │   ├── gptokeyb2.armhf
│   │   ├── innoextract.armhf
│   │   ├── libinterpose.armhf.so
│   │   ├── sdl2imgshow.armhf
│   │   ├── sdl_resolution.armhf
│   │   └── xdelta3.armhf
│   └── x86_64/                 # x86 64-bit binaries
│       ├── 7zzs.x86_64
│       ├── gptokeyb.x86_64
│       ├── gptokeyb2.x86_64
│       ├── innoextract.x86_64
│       ├── libinterpose.x86_64.so
│       ├── sdl2imgshow.x86_64
│       ├── sdl_resolution.x86_64
│       └── xdelta3.x86_64
├── platforms/                  # Platform-specific resources
│   ├── batocera/               # Batocera platform files
│   │   ├── control.txt
│   │   ├── gamecontrollerdb.txt
│   │   └── shGenerator.py
│   ├── knulli/                 # Knulli platform files
│   │   ├── control.txt
│   │   ├── gamecontrollerdb.txt
│   │   └── shGenerator.py
│   ├── miyoo/                  # Miyoo platform files
│   │   ├── control.txt
│   │   └── PortMaster.txt
│   ├── muos/                   # muOS platform files
│   │   ├── control.txt
│   │   ├── PortMaster.txt
│   │   ├── image_smash.txt
│   │   └── mount
│   ├── retrodeck/              # RetroDECK platform files
│   │   ├── control.txt
│   │   ├── PortMaster.txt
│   │   ├── liblzo2.so.2
│   │   ├── mount
│   │   └── unsquashfs
│   ├── trimui/                 # TrimUI platform files
│   │   ├── control.txt
│   │   ├── PortMaster.txt
│   │   ├── config.json
│   │   ├── icon.png
│   │   ├── image_smash.txt
│   │   └── update.txt
│   ├── libgl_*.txt             # Platform-specific OpenGL configs
│   ├── mod_*.txt               # Platform-specific modifications
│   ├── oga_controls            # OGA control binary
│   └── oga_controls_settings.txt
├── exlibs/                     # External Python libraries
├── libs/                       # Runtime libraries
├── pylibs/                     # Python libraries
├── resources/                  # GUI resources
├── runtimes/                   # Runtime environments
├── utils/                      # Utility scripts
├── control.txt                 # Main control script
├── device_info.txt             # Device detection script
├── funcs.txt                   # Common functions
├── PortMaster.sh               # Main launcher script
└── pugwash                     # Main GUI executable
```

## Binary Organization

All architecture-specific binaries are now organized under `archs/` by architecture:
- **aarch64**: ARM 64-bit binaries
- **armhf**: ARM 32-bit hard float binaries  
- **x86_64**: x86 64-bit binaries

Scripts reference these binaries using the `${DEVICE_ARCH}` variable:
```bash
$controlfolder/archs/${DEVICE_ARCH}/gptokeyb
```

## Platform Organization

All platform-specific resources are now organized under `platforms/`:
- Platform subdirectories (batocera/, knulli/, miyoo/, muos/, retrodeck/, trimui/)
- Platform configuration files (mod_*.txt, libgl_*.txt)
- Platform-specific binaries and scripts

Scripts reference these files using platform names:
```bash
source "${controlfolder}/platforms/mod_${CFW_NAME}.txt"
```

## Migration Notes

This reorganization was done to:
1. **Improve clarity**: Separate platform and architecture concerns
2. **Reduce clutter**: Move 20+ files from root to organized subdirectories
3. **Ease maintenance**: Clear structure makes it easier to add new platforms/architectures
4. **Maintain compatibility**: All existing scripts updated to use new paths

## Backward Compatibility

The reorganization maintains backward compatibility through:
- Updated path references in all core scripts
- Updated platform-specific control files
- Updated release build scripts
- Architecture detection remains unchanged
