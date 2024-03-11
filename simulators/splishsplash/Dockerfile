# Start from an official CUDA image from NVIDIA.
FROM nvidia/cuda:11.2.2-devel-ubuntu20.04

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install SPlisHSPlasH dependencies.
RUN apt-get update -y; \
    apt-get install -y git cmake xorg-dev freeglut3-dev build-essential

# Install Python 3.11.
RUN apt-get update -y; \
    apt-get install curl software-properties-common -y; \
    add-apt-repository ppa:deadsnakes/ppa; \
    apt-get install -y python3.11 python3.11-distutils; \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11; \
    rm -f /usr/bin/python && ln -s /usr/bin/python3.11 /usr/bin/python


# Clone SPlisHSPlasH repository.
WORKDIR /
RUN git clone https://github.com/InteractiveComputerGraphics/SPlisHSPlasH.git


# Build SPlisHSPlasH with GPU support.
RUN cmake \
    -S /SPlisHSPlasH -B /SPlisHSPlasH_GPU/build \
    -DUSE_GPU_NEIGHBORHOOD_SEARCH=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE=/SPlisHSPlasH_GPU/bin \
    -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=/SPlisHSPlasH_GPU/bin \
    -DUSE_PYTHON_BINDINGS=OFF \
    -DBuild_PartioViewer=OFF \
    -DBuild_FoamGenerator=OFF \
    -DBuild_VolumeSampling=OFF \
    -DBuild_MeshSkinning=OFF

WORKDIR /SPlisHSPlasH_GPU/build
RUN make -j 4

# Build SPlisHSPlasH without GPU suppport.
RUN cmake \
    -S /SPlisHSPlasH -B /SPlisHSPlasH_CPU/build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE=/SPlisHSPlasH_CPU/bin \
    -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=/SPlisHSPlasH_CPU/bin \
    -DUSE_PYTHON_BINDINGS=OFF \
    -DBuild_PartioViewer=OFF \
    -DBuild_FoamGenerator=OFF \
    -DBuild_VolumeSampling=OFF \
    -DBuild_MeshSkinning=OFF

WORKDIR /SPlisHSPlasH_CPU/build
RUN make -j 4

# Install gmsh.
RUN apt-get update -y; \
    apt-get install -y gmsh
