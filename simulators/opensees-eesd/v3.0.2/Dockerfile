# Base image with common build dependencies
FROM ubuntu:22.04 AS base
ENV DEBIAN_FRONTEND=noninteractive

# Build arguments and versions
ARG OPENSEES_VERSION=v3.7.1
ARG BASE_IMAGE=ubuntu:22.04
ARG PYTHON_VERSION=3.8
# System dependencies
RUN apt-get update && apt-get install -y \
    make \
    git \
    tcl8.6 \
    tcl8.6-dev \
    gcc \
    g++ \
    gfortran \
    python3-dev \
    liblapack-dev \
    libopenmpi-dev \
    libmkl-rt \
    openmpi-common=4.1.2-2ubuntu1 \
    libmkl-blacs-openmpi-lp64 \
    libarpack2-dev \
    libscalapack-openmpi-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and extract OpenSees source
WORKDIR /
RUN git clone https://github.com/eesd-epfl/OpenSees.git \
    && cd OpenSees \
    # go to commit ad85d455c3ad6626baeafed1729da240da5c5377
    && git checkout ad85d455c3ad6626baeafed1729da240da5c5377

WORKDIR /OpenSees/

COPY Makefile.def.EC2-UBUNTU /OpenSees/Makefile.def

RUN cp /usr/lib/x86_64-linux-gnu/libarpack.a /lib/libArpack.a && \
    make

COPY /example/Example2.tcl /src/examples/

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh
