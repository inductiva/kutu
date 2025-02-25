# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

ARG CM1_VERSION=18
ARG CM1_BASE_DIR=/cm1
ARG OPENMPI_PATH=/usr/lib/x86_64-linux-gnu/openmpi
ARG LIB_PATH=/usr/lib/x86_64-linux-gnu

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies 
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    openmpi-bin \
    libopenmpi-dev \
    wget \
    libhdf5-openmpi-dev \
    libnetcdf-dev \
    libomp-dev \
    libnetcdff-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for OpenMPI
ENV PATH=${OPENMPI_PATH}/bin:${PATH}
ENV LD_LIBRARY_PATH=${LIB_PATH}:${OPENMPI_PATH}/lib
ENV OMPI_MCA_btl_vader_single_copy_mechanism=none
ENV OMPI_FC=gfortran\
    FFLAGS=" -m64 -fallow-argument-mismatch -ffree-form -ffree-line-length-none -O2 -finline-functions -fno-range-check -Wno-line-truncation"

# Create working directory
WORKDIR ${CM1_BASE_DIR}

# Download and extract CM1
RUN wget https://www2.mmm.ucar.edu/people/bryan/cm1/cm1r${CM1_VERSION}.tar.gz && \
    tar xzf cm1r${CM1_VERSION}.tar.gz && \
    mv cm1r${CM1_VERSION}/* . && \
    rm -rf cm1r${CM1_VERSION} cm1r${CM1_VERSION}.tar.gz

    
# Compile CM1

# First, create a modified Makefile for MPI build
COPY ./Makefile src/Makefile

# Clean and compile MPI version
RUN cd src && make clean && make && \
    mv ../run/cm1.exe /bin/ && \
    make clean

    

    COPY ./test_sim.sh /home/test_sim.sh
    RUN chmod +x /home/test_sim.sh
# Set working directory to run directory
WORKDIR /cm1/run

# Set default command to print version info
CMD ["./cm1.exe", "-v"]