FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/openseespy-input-example.zip -P /home/ && \
    unzip /home/openseespy-input-example.zip -d /home/ && \
    rm /home/openseespy-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh


FROM ubuntu:22.04 AS build
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    python3-pip \
    liblapack-dev \
    libopenmpi-dev \
    openmpi-bin \
    libmkl-rt \
    openmpi-common=4.1.2-2ubuntu1 \
    libmkl-blacs-openmpi-lp64 \
    libscalapack-openmpi-dev \
    wget \
    libglu1-mesa-dev \
    libgl1-mesa-dev \
    libxmu-dev \
    libxi-dev \
    build-essential \
    cmake \
    libfreetype6-dev \
    tk-dev \
    python3-dev \
    rapidjson-dev \
    python3 \
    python3-numpy \
    git \
    python3-pip \
    libpcre2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install SWIG 4.2.1 from source
RUN cd / && \
    wget http://prdownloads.sourceforge.net/swig/swig-4.2.1.tar.gz && \
    tar -zxvf swig-4.2.1.tar.gz && \
    cd swig-4.2.1 && \
    ./configure && \
    make -j$(nproc) && \
    make install

# Install OpenCascade 7.8.1.1 from source
RUN cd / && \
    wget https://github.com/Open-Cascade-SAS/OCCT/archive/refs/tags/V7_8_1.tar.gz && \
    tar -xvzf V7_8_1.tar.gz && \
    cd OCCT-7_8_1 && \
    mkdir cmake-build && \
    cd cmake-build && \
    cmake -DINSTALL_DIR=/opt/occt781 -DBUILD_RELEASE_DISABLE_EXCEPTIONS=OFF .. && \
    make -j$(nproc) && \
    make install && \
    bash -c 'echo "/opt/occt781/lib" >> /etc/ld.so.conf.d/occt.conf' && \
    ldconfig

RUN pip install openseespy==3.7.1.2 && \
    pip install sees==0.0.25 && \
    pip install numpy && \
    pip install mpi4py && \
    pip install ifcopenshell && \
    pip install gmsh && \
    cp /usr/bin/python3 /usr/bin/python

RUN python3 -c "import numpy; print(numpy.get_include())" && \
    apt-get update && apt-get install -y python3-numpy


# Build pythonOCC
RUN cd / && \
    git clone https://github.com/tpaviot/pythonocc-core.git && \
    cd pythonocc-core && \
    mkdir cmake-build && cd cmake-build && \
    cmake -DOCCT_INCLUDE_DIR=/opt/occt781/include/opencascade \
          -DOCCT_LIBRARY_DIR=/opt/occt781/lib \
          -DCMAKE_BUILD_TYPE=Release \
          -DPYTHONOCC_INSTALL_DIRECTORY=/usr/local .. && \
    make -j$(nproc) && \
    make install

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/occt781/lib

COPY --from=test_env /home /home

