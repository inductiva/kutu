FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN curl https://storage.googleapis.com/inductiva-api-demo-files/dualsphysics-input-example.zip\ 
        --output /home/dualsphysics-input-example.zip && \
    unzip /home/dualsphysics-input-example.zip -d /home/ && \
    rm /home/dualsphysics-input-example.zip && \
    #Reduce Simulation time to 1 second
    sed -i 's/key="TimeMax" value="3"/key="TimeMax" value="1"/g' \
        /home/dualsphysics-input-example/config.xml

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

RUN wget -O DualSPHysics_v5.4.1.zip  https://storage.googleapis.com/inductiva-host-source-codes/DualSPHysics_v5.4.1.zip\
    && unzip /DualSPHysics_v5.4.1.zip && \
    rm -r /DualSPHysics_v5.4.1.zip \ 
        /DualSPHysics_v5.4.1/bin/windows \
        /DualSPHysics_v5.4.1/CHANGES.txt \
        /DualSPHysics_v5.4.1/examples/ \
        /DualSPHysics_v5.4.1/doc/ \
        /DualSPHysics_v5.4.1/Files_DualSPHysics_v5.4.1.pdf \
        /DualSPHysics_v5.4.1/src/VS \
        /DualSPHysics_v5.4.1/src/lib/vs2022/ \
        /DualSPHysics_v5.4.1/src_flexstruc/VS/ \
        /DualSPHysics_v5.4.1/src_flexstruc/lib/vs2022/ \
        /DualSPHysics_v5.4.1/src_extra/ \
        /DualSPHysics_v5.4.1/src_mphase/ 

# Build DualSPHysics.
WORKDIR /DualSPHysics_v5.4.1/src/source/build
RUN CC=gcc CXX=g++ cmake .. && make

FROM nvidia/cuda:11.7.1-runtime-ubuntu22.04

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
COPY --from=build /DualSPHysics_v5.4.1/src/source/../lib/linux_gcc/libdsphchrono.so /DualSPHysics_v5.4.1/src/source/../lib/linux_gcc/libdsphchrono.so
COPY --from=build /DualSPHysics_v5.4.1/src/source/../lib/linux_gcc/libChronoEngine.so /DualSPHysics_v5.4.1/src/source/../lib/linux_gcc/libChronoEngine.so

COPY --from=test_env /home /home
COPY --from=build /DualSPHysics_v5.4.1 /DualSPHysics_v5.4.1

# Set environment variable with path to DualSPHysics binaries.
ENV DUALSPHYSICS_BIN_DIR="/DualSPHysics_v5.4.1/bin/linux"
ENV PATH="${DUALSPHYSICS_BIN_DIR}:${PATH}"

WORKDIR /
COPY ./setup.sh /setup.sh
RUN chmod +x /setup.sh && \
    /setup.sh && \
    cp /DualSPHysics_v5.4.1/bin/linux/DualSPHysics5.2_linux64 /DualSPHysics_v5.4.1/bin/linux/dualsphysics