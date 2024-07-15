FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

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

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh