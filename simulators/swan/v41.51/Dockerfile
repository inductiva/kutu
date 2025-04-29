FROM ubuntu:22.04 AS test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/swan-input-example.zip -P /home/ && \
    unzip /home/swan-input-example.zip -d /home/ && \
    rm /home/swan-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Fetch base image of ubuntu with 77 MB. 
FROM intel/oneapi-hpckit:devel-ubuntu20.04 AS build

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive


# Environment variables and arguments for SWAN
ENV SWAN_HOME=/swan
ARG SWAN_VERSION=41.51
ARG SWAN_TMP=/tmp/swan
ENV SWAN_BIN=swan.exe

# Instal SWAN from source code
RUN mkdir ${SWAN_TMP}
WORKDIR ${SWAN_TMP}

# Download, build, and install SWAN

RUN wget https://storage.googleapis.com/inductiva-simulators-sources/swan/v${SWAN_VERSION}/swan${SWAN_VERSION}.tar.gz && \
    tar -xzf swan${SWAN_VERSION}.tar.gz --directory . --strip-components 1 && \
    mkdir build ${SWAN_HOME} && \
    cd build && \
    cmake .. \
        -DMPI=ON \
        -DNETCDF=ON \
        -DCMAKE_INSTALL_PREFIX=${SWAN_HOME} && \
    make && \
    make install && \
    cp bin/swan.exe bin/hcat.exe ../bin/swanrun ${SWAN_HOME} && \
    chmod +rx ${SWAN_HOME}/swanrun && \
    rm -rf ${SWAN_TMP} && \
    sed -i '2i set -e' ${SWAN_HOME}/swanrun && \
    sed -i 's/mpirun -np \$npmpi swan.exe/mpirun -np \$npmpi -machinefile machinefile swan.exe/' ${SWAN_HOME}/swanrun

ENV PATH ${SWAN_HOME}:$PATH

COPY --from=test_env /home /home
