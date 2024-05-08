FROM ubuntu:22.04 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/amr-wind-input-example.zip -P /home/ && \
    unzip /home/amr-wind-input-example.zip -d /home/ && \
    rm /home/amr-wind-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 as build

RUN apt update -qq && \
    apt install -y software-properties-common build-essential && \
    add-apt-repository ppa:git-core/ppa -y && \
    apt install -y libblas-dev liblapack-dev \
        libopenmpi-dev=4.1.2-2ubuntu1 \
        openmpi-bin=4.1.2-2ubuntu1 \
        gcc gfortran make \
        python3-pip \
        libomp-dev \
        cmake \
        wget \
        git && \
    # Fortran compiler
    export FC=/usr/bin/gfortran && \
    # Clone Openfast repository
    git clone --recursive --branch v1.4.0 https://github.com/Exawind/amr-wind.git amr-wind && \
    mkdir amr-wind/build && cd amr-wind/build && \
    cmake   -DAMR_WIND_ENABLE_OPENMP:BOOL=FALSE \
            -DCMAKE_BUILD_TYPE:STRING=RELEASE \
            -DAMR_WIND_ENABLE_MPI:BOOL=ON .. && \
    # Using -j may cause the build to fail
    make && \
    make install && \
    cd / && \
    rm -rf amr-wind

COPY --from=test_env /home /home
