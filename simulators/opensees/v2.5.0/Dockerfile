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
    python3-pip \
    liblapack-dev \
    libopenmpi-dev \
    openmpi-common \
    libmumps-dev \
    wget \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir /src/lib && \
    mkdir /src/bin


# Download and extract OpenSees source
WORKDIR /src
RUN wget https://github.com/OpenSees/OpenSees/archive/refs/tags/${OPENSEES_VERSION}.tar.gz \
    && tar xzf ${OPENSEES_VERSION}.tar.gz \
    && rm ${OPENSEES_VERSION}.tar.gz \
    && mv OpenSees-* OpenSees

COPY Makefile.def /src/OpenSees/Makefile.def

RUN cd /src/OpenSees && \
    make
