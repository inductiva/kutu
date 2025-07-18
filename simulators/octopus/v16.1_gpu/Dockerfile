FROM inductiva/kutu:base-image_v0.1.0 AS test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/octopus-input-example.zip -P /home/ && \
    unzip /home/octopus-input-example.zip -d /home/ && \
    rm /home/octopus-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM nvidia/cuda:11.7.1-devel-ubuntu22.04 AS build

ENV DEBIAN_FRONTEND=noninteractive
# Bug: https://gitlab.com/octopus-code/octopus/-/issues/900
ENV FCFLAGS_ELPA="-I/usr/include -I/usr/include/elpa/modules"
ENV FCFLAGS="-ffree-line-length-none"

RUN apt-get -y update && \
    apt-get -y install \
        autoconf \
        automake \
        build-essential \
        g++ \
        gcc \
        gfortran \
        git \
        imagemagick \
        gnuplot \
        libatlas-base-dev \
        libblas-dev \
        libboost-dev \
        libcgal-dev \
        libelpa-dev \
        libetsf-io-dev \
        libfftw3-dev \
        libgmp-dev \
        libgsl-dev \
        liblapack-dev \
        liblapack-dev \
        libmpfr-dev \
        libnetcdff-dev \
        libnlopt-dev \
        libopenmpi-dev \
        libscalapack-mpi-dev \
        libspfft-dev \
        libtool \
        libxc-dev \
        libyaml-dev \
        openscad \
        openctm-tools \
        pkg-config \
        procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    cd / && \
    git clone --branch 16.1 --single-branch https://gitlab.com/octopus-code/octopus.git && \
    cd octopus && \
    autoreconf --install && \
    ./configure --prefix=/  --enable-mpi --enable-openmp --with-blacs="-lscalapack-openmpi" --enable-cuda-mpi --enable-cuda --with-cuda-prefix=/usr/local/cuda-11.7 && \
    make -j && \
    make install && \
    cd /octopus && \
    rm -r src && \
    rm -r share && \
    rm -r doc && \
    rm -r testsuite


COPY --from=test_env /home /home