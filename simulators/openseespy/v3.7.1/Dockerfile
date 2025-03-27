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
    git \
    python3-pip \
    libpcre2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install openseespy==3.7.1.2 && \
    pip install sees==0.0.25 && \
    pip install numpy && \
    pip install mpi4py && \
    pip install ifcopenshell && \
    pip install gmsh && \
    cp /usr/bin/python3 /usr/bin/python

RUN cd / && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    /root/miniconda3/bin/conda install conda-forge::pythonocc-core && \
    #Copy OCC to our default python instalation
    #cant install pythonocc-core with pip
    #cant install mpi4py with conda
    cp -r /root/miniconda3/lib/python3.12/site-packages/OCC/ /usr/local/lib/python3.10/dist-packages/ && \
    cp /root/miniconda3/lib/* /lib/ -r && \
    rm -r /root/miniconda3/

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/occt781/lib

COPY --from=test_env /home /home

