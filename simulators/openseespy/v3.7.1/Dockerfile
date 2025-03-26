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

# Set environment variables
ENV PATH="/opt/conda/bin:$PATH"

# Download and install Anaconda
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2023.07-0-Linux-x86_64.sh -O /tmp/anaconda.sh && \
    bash /tmp/anaconda.sh -b -p /opt/conda && \
    rm /tmp/anaconda.sh

# Install packages in the base environment
RUN conda install -c conda-forge pythonocc-core=7.8.1.1

RUN pip install openseespy==3.7.1.2 && \
    pip install sees==0.0.25 && \
    pip install mpi4py && \
    pip install ifcopenshell && \
    pip install gmsh && \
    cp /usr/bin/python3 /usr/bin/python

COPY --from=test_env /home /home

