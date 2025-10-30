# PortMaster GUI - Dependency Diagrams

This document provides visual diagrams of the dependencies and execution flows in the PortMaster GUI repository.

## Table of Contents

1. [Build and Release Flow](#build-and-release-flow)
2. [Python Module Dependencies](#python-module-dependencies)
3. [Runtime Execution Flow](#runtime-execution-flow)
4. [Platform-Specific Builds](#platform-specific-builds)
5. [Script Interactions](#script-interactions)

---

## Build and Release Flow

This diagram shows the main build and release process, including how different scripts call each other.

```mermaid
graph TD
    A[do_release.sh] --> B[tools/pm_release.py]
    A --> C[msgfmt - Compile translations]
    A --> D[zip - Create pylibs.zip]
    A --> E[zip - Create PortMaster.zip]
    
    A --> F{Release Type?}
    F -->|stable| G[Create Installers]
    F -->|beta/alpha| H[Skip Installers]
    
    G --> I[tools/download_runtimes.sh]
    G --> J[makeself - Create installer]
    
    A --> K[tools/pm_version.py]
    
    B --> L[Update PORTMASTER_VERSION]
    B --> M[Update PORTMASTER_RELEASE_CHANNEL]
    
    K --> N[Generate version.json]
    K --> O[Calculate MD5 hash]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style K fill:#fff4e1
```

## Python Module Dependencies

This diagram shows how the main Python components depend on each other.

```mermaid
graph TD
    A[PortMaster/pugwash] --> B[harbourmaster]
    A --> C[utility]
    A --> D[pySDL2gui]
    A --> E[pugtheme]
    A --> F[pugscene]
    A --> G[sdl2]
    A --> H[requests]
    A --> I[png]
    A --> J[loguru]
    
    B --> B1[harbourmaster.harbour]
    B --> B2[harbourmaster.hardware]
    B --> B3[harbourmaster.platform]
    B --> B4[harbourmaster.source]
    B --> B5[harbourmaster.util]
    B --> B6[harbourmaster.config]
    B --> B7[harbourmaster.info]
    B --> B8[harbourmaster.captain]
    
    B1 --> B5
    B1 --> B4
    B1 --> B7
    B2 --> B5
    B3 --> B2
    B3 --> B5
    B4 --> B5
    B7 --> B5
    B8 --> B5
    
    B5 --> C[utility]
    B5 --> H[requests]
    B5 --> J[loguru]
    
    E --> D
    E --> H
    F --> D
    F --> E
    
    A -.-> K[exlibs/urllib3]
    A -.-> L[exlibs/certifi]
    H --> K
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style B1 fill:#e8f5e9
    style B2 fill:#e8f5e9
    style B3 fill:#e8f5e9
    style B4 fill:#e8f5e9
    style B5 fill:#e8f5e9
    style B6 fill:#e8f5e9
    style B7 fill:#e8f5e9
    style B8 fill:#e8f5e9
```

## Runtime Execution Flow

This diagram shows the main execution paths when PortMaster runs on a device.

```mermaid
graph TD
    A[PortMaster.sh] --> B{Platform Detection}
    
    B -->|RetroDECK| C[Load retrodeck config]
    B -->|muOS| D[Load muOS config]
    B -->|Batocera| E[Load Batocera config]
    B -->|Other| F[Load default config]
    
    C --> G[Source control.txt]
    D --> G
    E --> G
    F --> G
    
    G --> H[Source mod_$CFW_NAME.txt]
    G --> I[get_controls]
    
    H --> J{Autoinstall?}
    I --> J
    
    J -->|Yes| K[PortMasterDialog.txt]
    J -->|No| L[pugwash or harbourmaster]
    
    K --> M[Process autoinstall/*.zip]
    K --> N[Process autoinstall/*.squashfs]
    K --> O[Install runtimes.zip]
    
    M --> L
    N --> L
    O --> L
    
    L --> P[Start GUI]
    L --> Q[Start CLI]
    
    P --> R[Initialize SDL2]
    P --> S[Load Theme]
    P --> T[Create Scenes]
    
    Q --> U[harbourmaster CLI]
    
    style A fill:#e1f5ff
    style P fill:#fff4e1
    style Q fill:#fff4e1
    style L fill:#e8f5e9
```

## Platform-Specific Builds

This diagram shows how platform-specific builds are created from the base PortMaster.zip.

```mermaid
graph TD
    A[PortMaster.zip] --> B[do_muos_release.sh]
    A --> C[do_trimui_release.sh]
    A --> D[do_x86_64_release.sh]
    
    B --> E{Stable?}
    C --> F{Stable?}
    D --> G{Stable?}
    
    E -->|Yes| H[Download from GitHub]
    E -->|No| I[Use local PortMaster.zip]
    
    F -->|Yes| H
    F -->|No| I
    
    G -->|Yes| H
    G -->|No| I
    
    I --> J[Extract PortMaster.zip]
    H --> J
    
    B --> K[muOS specific structure]
    C --> L[TrimUI specific structure]
    D --> M[x86_64 specific structure]
    
    K --> N[Copy muos/control.txt]
    K --> O[Copy muos/PortMaster.txt]
    K --> P[Remove tasksetter]
    
    L --> Q[Copy trimui/control.txt]
    L --> R[Copy trimui/launch.sh]
    L --> S[Copy trimui/config.json]
    L --> T[Copy trimui/icon.png]
    
    M --> U[retrodeck specific structure]
    M --> V[Copy retrodeck/control.txt]
    M --> W[Copy retrodeck/PortMaster.txt]
    
    N --> X[zip muos.portmaster.zip]
    O --> X
    P --> X
    
    Q --> Y[zip trimui.portmaster.zip]
    R --> Y
    S --> Y
    T --> Y
    
    V --> Z[zip retrodeck.portmaster.zip]
    W --> Z
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#fff4e1
    style D fill:#fff4e1
```

## Script Interactions

This diagram shows the interactions between various build and utility scripts.

```mermaid
graph TD
    A[Developer Action] --> B{Action Type?}
    
    B -->|Translations| C[do_i18n.sh]
    B -->|Beta Release| D[do_beta.sh]
    B -->|Stable Release| E[do_stable.sh]
    B -->|Standard Release| F[do_release.sh]
    B -->|muOS Build| G[do_muos_release.sh]
    B -->|TrimUI Build| H[do_trimui_release.sh]
    B -->|x86_64 Build| I[do_x86_64_release.sh]
    
    C --> J[xgettext - Extract strings]
    C --> K[theme_msgfmt.py]
    C --> L[crowdin upload]
    C --> M[crowdin download]
    C --> N[msgfmt - Compile .mo files]
    
    D --> C
    D --> O[tools/pm_release.py beta]
    D --> P[git commit]
    
    E --> C
    E --> Q[tools/pm_release.py stable]
    E --> P
    
    F --> R[tools/pm_release.py]
    F --> S[msgfmt translations]
    F --> T[Create pylibs.zip]
    F --> U[Create PortMaster.zip]
    F --> V{stable?}
    
    V -->|Yes| W[Create Installers]
    V -->|No| X[tools/pm_version.py]
    
    W --> Y[tools/download_runtimes.sh]
    W --> Z[makeself installer]
    W --> X
    
    G --> AA[Extract PortMaster.zip]
    G --> AB[Configure for muOS]
    G --> AC[Create muos.portmaster.zip]
    
    H --> AA
    H --> AD[Configure for TrimUI]
    H --> AE[Create trimui.portmaster.zip]
    
    I --> AA
    I --> AF[Configure for x86_64/RetroDECK]
    I --> AG[Create retrodeck.portmaster.zip]
    
    style A fill:#e1f5ff
    style C fill:#fff4e1
    style F fill:#e8f5e9
    style R fill:#ffe4e1
    style X fill:#ffe4e1
```

## Harbourmaster Module Architecture

This diagram shows the internal structure of the harbourmaster library.

```mermaid
graph TD
    A[harbourmaster/__init__.py] --> B[harbour.py - HarbourMaster class]
    A --> C[hardware.py - Device detection]
    A --> D[platform.py - Platform abstraction]
    A --> E[source.py - Port sources]
    A --> F[util.py - Utilities]
    A --> G[config.py - Configuration]
    A --> H[info.py - Port information]
    A --> I[captain.py - Port management]
    
    B --> J[Port Installation]
    B --> K[Port Uninstallation]
    B --> L[Source Management]
    B --> M[Runtime Management]
    
    C --> N[Device Info Detection]
    C --> O[Hardware Profiles]
    
    D --> P[Platform Detection]
    D --> Q[Platform Hooks]
    D --> R[CFW Detection]
    
    E --> S[Source Loading]
    E --> T[Port Listing]
    E --> U[Source Updates]
    
    F --> V[File Operations]
    F --> W[Download/Fetch]
    F --> X[Hash Verification]
    F --> Y[Callbacks]
    
    G --> Z[Default Paths]
    G --> AA[Configuration Constants]
    
    H --> AB[Port Metadata]
    H --> AC[Port JSON Parsing]
    H --> AD[Port Validation]
    
    I --> AE[Port Scripts]
    I --> AF[Port Execution]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style F fill:#e8f5e9
```

## GUI Architecture

This diagram shows how the GUI components interact.

```mermaid
graph TD
    A[pugwash] --> B[ThemeEngine]
    A --> C[Scene Manager]
    A --> D[HarbourMaster]
    
    B --> E[Theme Loading]
    B --> F[Color Schemes]
    B --> G[ThemeDownloader]
    
    C --> H[MainMenuScene]
    C --> I[PortsListScene]
    C --> J[PortInfoScene]
    C --> K[SettingsScene]
    C --> L[ThemesScene]
    C --> M[FilterScene]
    
    H --> N[pySDL2gui widgets]
    I --> N
    J --> N
    K --> N
    L --> N
    M --> N
    
    N --> O[Button]
    N --> P[TextBox]
    N --> Q[ImageBox]
    N --> R[ScrollBox]
    N --> S[ProgressBar]
    
    D --> T[Port Operations]
    T --> U[Download Port]
    T --> V[Install Port]
    T --> W[Update Port]
    T --> X[Uninstall Port]
    
    A --> Y[SDL2 Event Loop]
    Y --> Z[Input Handling]
    Y --> AA[Rendering]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#ffe4e1
```

## File Dependencies

This diagram shows key file dependencies in the repository.

```mermaid
graph TD
    A[PortMaster/] --> B[pugwash - Main GUI]
    A --> C[harbourmaster - CLI tool]
    A --> D[PortMaster.sh - Launcher]
    A --> E[pylibs/]
    A --> F[exlibs/]
    
    E --> G[harbourmaster/]
    E --> H[pugtheme.py]
    E --> I[pugscene.py]
    E --> J[pySDL2gui.py]
    E --> K[utility.py]
    E --> L[locales/]
    E --> M[resources/]
    
    F --> N[urllib3/]
    F --> O[certifi/]
    F --> P[Other bundled libs]
    
    D --> Q[control.txt]
    D --> R[mod_*.txt files]
    D --> S[PortMasterDialog.txt]
    D --> T[funcs.txt]
    
    A --> U[Platform dirs]
    U --> V[muos/]
    U --> W[trimui/]
    U --> X[batocera/]
    U --> Y[knulli/]
    U --> Z[retrodeck/]
    U --> AA[miyoo/]
    
    V --> AB[control.txt]
    V --> AC[PortMaster.txt]
    V --> AD[shGenerator.py]
    
    W --> AB
    W --> AC
    W --> AE[config.json]
    W --> AF[icon.png]
    
    X --> AD
    Y --> AD
    
    Z --> AB
    Z --> AC
    
    style A fill:#e1f5ff
    style E fill:#fff4e1
    style G fill:#e8f5e9
```

---

## Notes

### Build Scripts
- **do_release.sh**: Main release script that creates PortMaster.zip and optionally installers
- **do_i18n.sh**: Handles internationalization - extracts, uploads, downloads, and compiles translations
- **do_beta.sh** / **do_stable.sh**: Simplified scripts that call do_i18n.sh and set release channel
- **do_muos_release.sh** / **do_trimui_release.sh** / **do_x86_64_release.sh**: Create platform-specific builds

### Python Tools
- **tools/pm_release.py**: Updates version numbers and release channel in pugwash
- **tools/pm_version.py**: Generates version.json with MD5 hashes for release
- **tools/installer.sh**: Installation script packaged with makeself installers
- **theme_msgfmt.py**: Extracts translatable strings from themes

### Core Components
- **PortMaster/pugwash**: Main GUI application written in Python with SDL2
- **PortMaster/harbourmaster**: CLI tool for port management
- **PortMaster/PortMaster.sh**: Shell script launcher that detects platform and starts the appropriate tool

### Libraries
- **pylibs/harbourmaster/**: Core library for port management (shared by GUI and CLI)
- **pylibs/pySDL2gui.py**: Custom GUI framework built on PySDL2
- **pylibs/pugtheme.py**: Theme engine supporting multiple color schemes
- **pylibs/pugscene.py**: Scene management for different GUI screens
- **exlibs/**: Bundled third-party libraries (urllib3, certifi, etc.)

### Platform Support
The repository supports multiple platforms through platform-specific configuration:
- muOS
- TrimUI
- Batocera
- Knulli
- RetroDECK
- Miyoo
- Generic Linux devices

Each platform has its own configuration files in `PortMaster/<platform>/` directories.
