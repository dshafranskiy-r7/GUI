FROM python:3.12

# Update package list and install basic utilities
RUN apt-get update
RUN apt-get install -y \
    unzip \
    systemd \
    usbutils
#     curl \
#     wget \
#     git \
#     vim \
#     && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app/PortMaster/

COPY PortMaster.zip /tmp/

RUN unzip /tmp/PortMaster.zip -d /app

RUN cd /app/PortMaster/ && bash -x PortMaster.sh


# Create required directories for PortMaster
RUN mkdir -p /roms/ports/PortMaster/autoinstall \
    && mkdir -p /roms/ports/PortMaster/utils \
    && mkdir -p /dev

RUN cp /app/PortMaster/control.txt /roms/ports/PortMaster/control.txt
RUN cp /app/PortMaster/funcs.txt /roms/ports/PortMaster/funcs.txt
RUN cp /app/PortMaster/device_info.txt /roms/ports/PortMaster/device_info.txt


RUN echo "0.1.0" > /roms/ports/PortMaster/version

# Create required files
RUN touch /roms/ports/PortMaster/log.txt \
    && touch /roms/ports/PortMaster/utils/pmsplash.txt \
    && touch /dev/tty0


# Keep container running
CMD ["bash"]
# CMD ["/app/PortMaster/PortMaster.sh"]