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
    g++ \
    gcc \
    git \
    wget \
    cmake \
    tk-dev \
    python3 \
    gfortran \
    libmkl-rt \
    libxi-dev \
    libxmu-dev \
    libxcursor1 \
    openmpi-bin \
    python3-dev \
    python3-pip \
    libpcre2-dev \
    liblapack-dev \
    rapidjson-dev \
    libopenmpi-dev \
    build-essential \
    libgl1-mesa-dev \
    libfreetype6-dev \
    libglu1-mesa-dev \
    libscalapack-openmpi-dev \
    libmkl-blacs-openmpi-lp64 \
    openmpi-common=4.1.2-2ubuntu1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install openseespy==3.7.1.2 && \
    pip install sees==0.0.25 && \
    pip install numpy pandas mpi4py ifcopenshell gmsh && \
    cp /usr/bin/python3 /usr/bin/python

RUN cd / && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    /root/miniconda3/bin/conda install conda-forge::pythonocc-core && \
    #Copy OCC to our default python instalation
    #cant install pythonocc-core with pip
    #cant install mpi4py with conda
    cp -r /root/miniconda3/lib/python3.12/site-packages/OCC/ /usr/local/lib/python3.10/dist-packages/ && \
    rm -r /root/miniconda3/lib/terminfo && \
    cp /root/miniconda3/lib/* /lib/ -r && \
    rm -r /root/miniconda3/

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/occt781/lib:/usr/lib/x86_64-linux-gnu/

COPY --from=test_env /home /home

