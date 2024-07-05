FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        software-properties-common && \

    add-apt-repository ppa:git-core/ppa -y && \ 
    add-apt-repository ppa:deadsnakes/ppa && \

    apt-get install -y \
        build-essential \
        # fftw3 - Fourier transforms
        libfftw3-dev \
        pkg-config \
        fftw3 \
        # OpenMPI - Message Passing Interface
        openmpi-common=4.1.2-2ubuntu1 \
        libopenmpi-dev=4.1.2-2ubuntu1 \
        openmpi-bin=4.1.2-2ubuntu1 \
        # I might need to install ssh later
        openssh-client \
        # compilers
        gfortran-10 \
        gfortran \
        g++-10 \
        gcc-10 \
        gcc \
        g++ \
        # python
        python3.11-distutils \
        python3-pip \
        python3.11 \
        # other packages
        libscalapack-openmpi-dev \
        libgl1-mesa-glx \
        libopenblas-dev \
        libnetcdff-dev \
        freeglut3-dev \
        liblapack-dev \
        libnetcdf-dev \
        libglu1-mesa \
        libblas-dev \
        libomp-dev \
        liblapack3 \
        libx11-6 \
        libgomp1 \
        xorg-dev \
        libxmu6 \
        xvfb \
        gmsh \
        flex \
        #utilities
        unzip \
        cmake \
        make \
        curl \
        vim \
        git \
        wget

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh