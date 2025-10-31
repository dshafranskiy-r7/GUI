# PortMaster Docker Testing Environment

This Dockerfile provides a testing environment for building and running PortMaster.

## What it does

The Dockerfile:
1. Builds PortMaster using `do_release.sh` (creates PortMaster.zip)
2. Builds the x86_64 specific release using `do_x86_64_release.sh` (creates retrodeck.portmaster.zip)
3. Sets up the required directory structure at `/roms/ports/PortMaster`
4. Extracts and configures PortMaster in `/app/PortMaster`
5. Runs automated tests to verify the build

## Building the Docker Image

```bash
docker build -t portmaster-test .
```

This will:
- Install required dependencies (zip, unzip, wget, gettext, jq, SDL2 libraries)
- Run both build scripts
- Create all necessary directories and configuration files
- Take approximately 5-10 minutes depending on your system

## Running the Container

To run the default tests:
```bash
docker run --rm portmaster-test
```

This will display:
- Build artifacts (PortMaster.zip and retrodeck.portmaster.zip)
- Device information from harbourmaster CLI
- Success confirmation

Expected output includes:
```
PortMaster Build Test
Build artifacts:
-rw-r--r-- 1 root root 23M ... /build/PortMaster.zip
-rw-r--r-- 1 root root 23M ... /build/retrodeck.portmaster.zip

Testing harbourmaster CLI:
...
All tests passed!
```

## Using harbourmaster CLI

To run harbourmaster with different commands:
```bash
# List all available ports
docker run --rm portmaster-test ./harbourmaster --quiet list

# Show device information
docker run --rm portmaster-test ./harbourmaster device_info

# List available runtimes
docker run --rm portmaster-test ./harbourmaster runtime_list

# Show help
docker run --rm portmaster-test ./harbourmaster help
```

## Running PortMaster.sh

The PortMaster.sh script can be run in the container:

```bash
docker run --rm portmaster-test bash -c "./PortMaster.sh; echo Exit code: \$?"
```

Note: The GUI (pugwash) requires SDL2 rendering which is not available in a headless Docker environment. The script will log an SDL error but still exits with code 0 (success), which is the expected behavior for testing purposes.

## Running an Interactive Shell

To explore the container interactively:
```bash
docker run --rm -it portmaster-test /bin/bash
```

Once inside, you can:
- Explore `/app/PortMaster/` - Main PortMaster installation
- Check `/build/` - Build directory with source files and build artifacts
- Test `/roms/ports/PortMaster/` - PortMaster control folder with configuration
- Run `./harbourmaster` - CLI tool for managing ports
- Run `./pugwash --help` - View pugwash options (GUI requires display)

## Directory Structure

- `/app/PortMaster/` - Main PortMaster installation with all binaries and libraries
- `/roms/ports/PortMaster/` - PortMaster control folder with configuration (symlinked to main installation)
- `/build/` - Build directory containing:
  - `PortMaster.zip` - Standard PortMaster release
  - `retrodeck.portmaster.zip` - x86_64 specific release for RetroDECK

## Exit Codes

The container is designed to exit with code 0 (success) when running the default command, indicating that:
- Both build scripts (do_release.sh and do_x86_64_release.sh) completed successfully
- PortMaster.zip and retrodeck.portmaster.zip were created
- The harbourmaster CLI is functional
- All basic functionality tests passed

## Troubleshooting

### Build Failures
If the build fails, check:
- Docker has enough disk space (needs ~2GB)
- All dependencies are installed correctly
- Internet connectivity for downloading build tools

### SDL Errors
SDL errors are expected in a headless Docker environment. The container uses dummy SDL drivers for testing. These errors don't prevent the scripts from completing successfully (exit code 0).

### Missing Files
If files are missing after build:
```bash
# Check build artifacts
docker run --rm portmaster-test ls -lh /build/

# Check extracted files
docker run --rm portmaster-test ls -lh /app/PortMaster/
```
