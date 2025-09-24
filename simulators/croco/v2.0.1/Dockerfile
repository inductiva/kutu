FROM ubuntu:16.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gfortran \
                    make \
                    libopenmpi-dev \
                    libhdf5-openmpi-dev \
                    libnetcdf-dev \
                    libnetcdff-dev \
                    bc \
                    git \
                    curl \
                    netcdf-bin \
                    nco \
                    unzip \
                    wget \
                    sudo \
                    vim \
                    octave \
                    python3 \
                    octave-octcdf && \
    apt-get clean -y

RUN cd / && \
    wget https://gitlab.inria.fr/croco-ocean/croco/-/archive/v2.0.0/croco-v2.0.0.zip && \
    unzip croco-v2.0.0.zip && \
    rm croco-v2.0.0.zip && \
    wget https://gitlab.inria.fr/croco-ocean/croco_tools/-/archive/v2.0.0/croco_tools-v2.0.0.zip && \
    unzip croco_tools-v2.0.0.zip && \
    rm croco_tools-v2.0.0.zip && \
    wget https://gitlab.inria.fr/croco-ocean/croco_pytools/-/archive/v1.0.1/croco_pytools-v1.0.1.zip && \
    unzip croco_pytools-v1.0.1.zip && \
    rm croco_pytools-v1.0.1.zip && \
    mv croco-v2.0.0 croco && \
    mv croco_tools-v2.0.0 croco_tools && \
    mv croco_pytools-v1.0.1 croco_pytools && \
    sed -i 's/CROCO_DIR=$PWD/CROCO_DIR=\/croco\//g' /croco/create_config.bash && \
    sed -i 's/TOOLS_DIR=${PWD}\/..\/croco_tools/TOOLS_DIR=\/croco_tools/g' /croco/create_config.bash && \
    sed -i "s|\${TOOLS_DIR}/DATASETS_CROCOTOOLS/|\${PWD}/DATASETS_CROCOTOOLS/|g" /croco/create_config.bash && \
    sed -i "s/netcdf.setDefaultFormat('FORMAT_NETCDF4');/%netcdf.setDefaultFormat('FORMAT_NETCDF4');/" /croco_tools/crocotools_param.m


COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh