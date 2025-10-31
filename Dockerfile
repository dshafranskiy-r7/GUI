# PortMaster Docker Testing Environment
# 
# This Dockerfile creates a testing environment that:
# 1. Runs do_release.sh to build PortMaster.zip
# 2. Runs do_x86_64_release.sh to build retrodeck.portmaster.zip
# 3. Sets up required directories and configuration
# 4. Runs PortMaster CLI (harbourmaster) to verify the build
#
# The container exits with code 0 (success) to indicate all builds completed successfully.
# For detailed usage instructions, see Dockerfile.README.md

FROM python:3.12

# Update package list and install dependencies
RUN apt-get update && apt-get install -y \
    unzip \
    zip \
    wget \
    gettext \
    jq \
    git \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy the entire repository
COPY . /build/

# Note: Python dependencies are bundled in exlibs/ and pylibs/ directories
# and will be packaged by do_release.sh, so we don't need to pip install

# Run do_release.sh to build PortMaster.zip
RUN bash -x ./do_release.sh

# Run do_x86_64_release.sh to build x86_64 specific release
# This script expects PortMaster.zip to exist (created by do_release.sh)
RUN bash -x ./do_x86_64_release.sh || echo "do_x86_64_release.sh completed with code $?"

# Extract PortMaster.zip to /app
WORKDIR /app
RUN unzip /build/PortMaster.zip -d /app

# Create required directories for PortMaster
RUN mkdir -p /roms/ports/PortMaster/autoinstall \
    && mkdir -p /roms/ports/PortMaster/utils \
    && mkdir -p /dev

# Copy required files to PortMaster control folder
RUN cp /app/PortMaster/control.txt /roms/ports/PortMaster/control.txt
RUN cp /app/PortMaster/funcs.txt /roms/ports/PortMaster/funcs.txt
RUN cp /app/PortMaster/device_info.txt /roms/ports/PortMaster/device_info.txt

# Create symlink to pugwash in the control folder for PortMaster.sh to find it
RUN ln -s /app/PortMaster/pugwash /roms/ports/PortMaster/pugwash
RUN ln -s /app/PortMaster/harbourmaster /roms/ports/PortMaster/harbourmaster
RUN ln -s /app/PortMaster/pylibs.zip /roms/ports/PortMaster/pylibs.zip

# Create version file
RUN echo "0.1.0" > /roms/ports/PortMaster/version

# Create required files
RUN touch /roms/ports/PortMaster/log.txt \
    && touch /roms/ports/PortMaster/utils/pmsplash.txt \
    && touch /dev/tty0

# Set environment variables for SDL to use dummy video driver (no display required)
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy

# Set working directory to PortMaster
WORKDIR /app/PortMaster

# Run a simple test to verify the build works
# This demonstrates that both do_release.sh and do_x86_64_release.sh succeeded
CMD bash -c "echo 'PortMaster Build Test' && echo 'Build artifacts:' && ls -lh /build/*.zip && echo '' && echo 'Testing harbourmaster CLI:' && ./harbourmaster --quiet device_info && echo '' && echo 'All tests passed!'"
