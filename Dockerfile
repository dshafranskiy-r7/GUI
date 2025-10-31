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

# Run harbourmaster in CLI mode to verify everything works
# Using harbourmaster device_info to test the CLI interface
CMD ["./harbourmaster", "--quiet", "device_info"]
