FROM ubuntu:22.04 AS build

RUN apt-get update && \
    apt-get install -y \
    wget \
    xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Download and install Blender 4.5.4
RUN wget https://download.blender.org/release/Blender4.5/blender-4.5.4-linux-x64.tar.xz && \
    tar -xf blender-4.5.4-linux-x64.tar.xz && \
    mv blender-4.5.4-linux-x64 /opt/blender && \
    rm blender-4.5.4-linux-x64.tar.xz


FROM ubuntu:22.04

# Copy Blender installation
COPY --from=build /opt/blender /opt/blender

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y \
    libgl1 \
    libglu1-mesa \
    libfontconfig1 \
    libfreetype6 \
    libasound2 \
    libpulse0 \
    libdrm2 \
    libgbm1 \
    libegl1-mesa && \
    rm -rf /var/lib/apt/lists/*

# Create symlink for blender command
RUN ln -s /opt/blender/blender /usr/local/bin/blender

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

