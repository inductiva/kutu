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
    && rm -rf /var/lib/apt/lists/*

RUN pip install openseespy==3.7.1.2 && \
    pip install sees==0.0.25 && \
    pip install mpi4py && \
    pip install ifcopenshell && \
    pip install gmsh && \
    cp /usr/bin/python3 /usr/bin/python

COPY --from=test_env /home /home

