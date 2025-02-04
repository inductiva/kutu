# Base image with common build dependencies
FROM ubuntu:22.04 AS base
ENV DEBIAN_FRONTEND=noninteractive

# Build arguments and versions
ARG OPENSEES_VERSION=v3.7.1
ARG BASE_IMAGE=ubuntu:22.04
ARG PYTHON_VERSION=3.8
# System dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    g++ \
    gfortran \
    python3-pip \
    liblapack-dev \
    libopenmpi-dev \
    libmkl-rt \
    openmpi-common=4.1.2-2ubuntu1 \
    libmkl-blacs-openmpi-lp64 \
    libscalapack-openmpi-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Conan
RUN pip install "conan<2.0"

# Download and extract OpenSees source
WORKDIR /src
RUN wget https://github.com/OpenSees/OpenSees/archive/refs/tags/${OPENSEES_VERSION}.tar.gz \
    && tar xzf ${OPENSEES_VERSION}.tar.gz \
    && rm ${OPENSEES_VERSION}.tar.gz \
    && cp /usr/local/bin/conan /bin \
    && mv OpenSees-* opensees

WORKDIR /src/opensees
RUN apt-get update && apt-get install -y \
    libmumps-dev 

ENV CXXFLAGS="-fpermissive"

# Build OpenSees
RUN mkdir build \
    && cd build \
    && conan install .. --build missing > build.log \
    && cmake .. \
        -DMUMPS_DIR=/usr/lib/x86_64-linux-gnu \
        -DMUMPS_INCLUDE_DIR=/usr/include \
        -Darith=d -DCMAKE_MSVC_RUNTIME_LIBRARY="MultiThreaded" \
        -DOPENMPI=TRUE\
        -DSCALAPACK_LIBRARIES="/usr/lib/x86_64-linux-gnu/libscalapack-openmpi.so;/usr/lib/x86_64-linux-gnu/libmkl_blacs_openmpi_lp64.so" \
    && cmake --build . --target OpenSeesMP -j4 \
    && cmake --build . --target OpenSees -j4 \
    && cmake --build . --target OpenSeesPy -j4 \
    && mv ./lib/OpenSeesPy.so ./opensees.so \
    && mv ./bin/OpenSeesMP /bin


RUN mkdir -p /usr/lib/tcl8.6/* && \
    cp -r /src/opensees/build/lib/tcl8.6/* /usr/lib/tcl8.6/

COPY /example/Example2.tcl /src/examples/



COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh


CMD ["Opensees"]