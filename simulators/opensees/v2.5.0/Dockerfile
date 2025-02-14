# Base image with common build dependencies
FROM ubuntu:14.04 AS base
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/src
ENV CXXFLAGS="-fpermissive"

# Build arguments and versions
ARG OPENSEES_VERSION=v2.5.0
# System dependencies
RUN apt-get update && apt-get install -y \
    tcl8.5-dev \
    tcl8.5 \
    tk8.5-dev \
    cmake \
    gcc \
    g++ \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libopenblas-dev \
    libarpack2-dev \
    libparpack2-dev \
    libarpack++2-dev \
    libsuitesparse-dev \
    python3-pip \
    libopenmpi-dev \
    openmpi-common \
    libmumps-dev \
    wget \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir /src && \
    mkdir /src/lib && \
    mkdir /src/bin


# Download and extract OpenSees source
WORKDIR /src
RUN wget https://github.com/OpenSees/OpenSees/archive/refs/tags/${OPENSEES_VERSION}.tar.gz \
    && tar xzf ${OPENSEES_VERSION}.tar.gz \
    && rm ${OPENSEES_VERSION}.tar.gz \
    && mv OpenSees-* OpenSees && \
    cd OpenSees && \
    cp MAKES/Makefile.def.EC2-UBUNTU . && \
    mv Makefile.def.EC2-UBUNTU Makefile.def && \
    sed -i 's|HOME\s*=\s*/home/ubuntu|HOME = /src|' Makefile.def && \
    sed -i 's|SUPERLUdir\s*=\s*\$(HOME)/OpenSees/OTHER/SuperLU_4.1/SRC|SUPERLUdir = \$(HOME)/OpenSees/OTHER/SuperLU_5.0/SRC|' Makefile.def && \
    sed -i 's|TCL_LIBRARY = /usr/lib/libtcl8.5.so|TCL_LIBRARY = /usr/lib/x86_64-linux-gnu/libtcl8.5.so|' Makefile.def && \
    sed -i 's|TCL_INCLUDES = -I/usr/include/tcl8.5|TCL_INCLUDES = -I/usr/include/tcl8.5/tcl-private/generic|' Makefile.def

RUN cd /src/OpenSees && \
    make && \
    cp /src/bin/OpenSees /src/bin/OpenSeesMP && \
    mkdir /home/opensees-input-example && \
    cp /src/OpenSees/EXAMPLES/verification/PlanarTruss.tcl /home/opensees-input-example/PlanarTruss.tcl


ENV PATH="/src/bin:${PATH}"

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh
