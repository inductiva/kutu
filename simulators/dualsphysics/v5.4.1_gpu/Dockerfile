FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN curl https://storage.googleapis.com/inductiva-api-demo-files/dualsphysicsv5.4.1-input-example.zip\ 
        --output /home/dualsphysicsv5.4.1-input-example.zip && \
    unzip /home/dualsphysicsv5.4.1-input-example.zip -d /home/ && \
    rm /home/dualsphysicsv5.4.1-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Start from an image provided by NVIDIA with CUDA 11.7.
FROM nvidia/cuda:11.7.1-devel-ubuntu22.04 as build

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        software-properties-common && \
    add-apt-repository ppa:git-core/ppa -y && \ 
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y \
    # Development Tools
    build-essential \
    pkg-config \
    cmake \
    make \
    wget \
    curl \
    vim \
    git \
    # Compilers and Libraries
    libopenmpi-dev=4.1.2-2ubuntu1 \
    libscalapack-openmpi-dev \
    libopenblas-dev \
    libnetcdff-dev \
    liblapack-dev \
    libnetcdf-dev \
    libfftw3-dev \
    gfortran-10 \
    libblas-dev \
    libomp-dev \
    liblapack3 \
    gfortran \
    libgomp1 \
    g++-10 \
    gcc-10 \
    gcc \
    g++ \
    # MPI (Message Passing Interface)
    openmpi-common=4.1.2-2ubuntu1 \
    openmpi-bin=4.1.2-2ubuntu1 \
    # Python
    python3.11-distutils \
    python3-pip \
    python3.11 \
    # X11 and Graphics Libraries
    libgl1-mesa-glx \
    freeglut3-dev \
    libglu1-mesa \
    libx11-6 \
    xorg-dev \
    libxmu6 \
    xvfb \
    # Miscellaneous
    openssh-client \
    fftw3 \
    gmsh \
    flex \
    unzip

# Clone the DualSPHysics repository.
WORKDIR /

RUN wget -O DualSPHysics_v5.4.1zip  https://storage.googleapis.com/inductiva-host-source-codes/DualSPHysics_v5.4.1.zip\
    && unzip /DualSPHysics_v5.4.1zip && \
    mv /DualSPHysics_v5.4 /DualSPHysics && \
    cd /DualSPHysics/src/source/ && \
    sed -i 's/^CUDAVER=12/CUDAVER=11/' Makefile && \
    sed -i 's|DIRTOOLKIT=/exports/opt/NVIDIA/cuda-11.7|DIRTOOLKIT=/usr/local/cuda-11.7|' Makefile && \
    make && \
    make -f Makefile_cpu

    
FROM nvidia/cuda:11.7.1-runtime-ubuntu22.04

# Avoid user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies, Python, pip, and Python packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    && pip3 install --no-cache-dir \
    vtk \
    numpy \
    numba \
    scikit-image \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set default python command
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY ./script/vtk_to_obj.py /python_script/vtk_to_obj.py

# COPY libgomp libraries from the build stage.
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libc.so.6 /usr/lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libm.so.6 /usr/lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libdl.so.2 /usr/lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/librt.so.1 /usr/lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libpthread.so.0 /usr/lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /DualSPHysics/bin/linux/libdsphchrono.so /DualSPHysics/bin/linux/libdsphchrono.so
COPY --from=build /DualSPHysics/bin/linux/libChronoEngine.so /DualSPHysics/bin/linux/libChronoEngine.so

COPY --from=test_env /home /home
COPY --from=build /DualSPHysics /DualSPHysics

# Set environment variable with path to DualSPHysics binaries.
ENV DUALSPHYSICS_BIN_DIR="/DualSPHysics/bin/linux"
ENV PATH="${DUALSPHYSICS_BIN_DIR}:${PATH}"
ENV LD_LIBRARY_PATH=/DualSPHysics/bin/linux:$LD_LIBRARY_PATH


WORKDIR /
COPY ./setup.sh /setup.sh
RUN chmod +x /setup.sh && \
    /setup.sh && \
    cp /DualSPHysics/bin/linux/DualSPHysics5.4_linux64 /DualSPHysics/bin/linux/dualsphysics