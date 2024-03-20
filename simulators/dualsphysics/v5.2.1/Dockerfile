# Start from an image provided by NVIDIA with CUDA 11.7.
FROM nvidia/cuda:11.7.1-devel-ubuntu22.04

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install git and cmake.
RUN apt-get update -y \
    && apt-get install -y git cmake wget unzip

# Install Python 3.11.
RUN apt-get update -y; \
    apt-get install curl software-properties-common -y; \
    add-apt-repository ppa:deadsnakes/ppa; \
    apt-get install -y python3.11 python3.11-distutils; \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11; \
    rm -f /usr/bin/python && ln -s /usr/bin/python3.11 /usr/bin/python

# Clone the DualSPHysics repository.
WORKDIR /
RUN wget -O DualSPHysics_v5.2.zip  https://storage.googleapis.com/inductiva-host-source-codes/DualSPHysics_v5.2.1.zip\
    && unzip /DualSPHysics_v5.2.zip

# Build DualSPHysics.
WORKDIR /DualSPHysics_v5.2/src/source/build
RUN CC=gcc CXX=g++ cmake ..
RUN make

# Set environment variable with path to DualSPHysics binaries.
ENV DUALSPHYSICS_BIN_DIR="/DualSPHysics_v5.2/bin/linux"

WORKDIR /

COPY ./setup.sh /setup.sh
RUN chmod +x /setup.sh
RUN /setup.sh
