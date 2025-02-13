# Base image with common build dependencies
FROM ubuntu:14.04 AS base
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/src
# Build arguments and versions
ARG OPENSEES_VERSION=v2.5.0
ARG BASE_IMAGE=ubuntu:22.04
ARG PYTHON_VERSION=3.8
# System dependencies
RUN apt-get update && apt-get install -y \
    tcl8.5-dev \
    tk8.5-dev \
    cmake \
    gcc \
    g++ \
    gfortran \
    python3-pip \
    liblapack-dev \
    libopenmpi-dev \
    openmpi-common \
    wget \
    && rm -rf /var/lib/apt/lists/*


# Download and extract OpenSees source
WORKDIR /src
RUN wget https://github.com/OpenSees/OpenSees/archive/refs/tags/${OPENSEES_VERSION}.tar.gz \
    && tar xzf ${OPENSEES_VERSION}.tar.gz \
    && rm ${OPENSEES_VERSION}.tar.gz \
    && mv OpenSees-* OpenSees

RUN apt-get update && apt-get install -y \
    libmumps-dev

COPY Makefile.def /src/OpenSees/Makefile.def

RUN cd /src/OpenSees && \
    make

ENV CXXFLAGS="-fpermissive"