FROM ubuntu:22.04 as test_env

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
FROM ubuntu:22.04

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install updates and essential tools to build and install Open MPI and SWAN.
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget ssh build-essential

# Install gcc-10 and set it as the default GNU compiler.
RUN apt-get install -y gcc-10 g++-10 gfortran-10 && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 10 && \
    update-alternatives --set gcc /usr/bin/gcc-10 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10 && \
    update-alternatives --set g++ /usr/bin/g++-10 && \
    update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-10 10 && \
    update-alternatives --set gfortran /usr/bin/gfortran-10


# Set Open MPI options.
ENV OPENMPI_HOME=/openmpi
ARG OPENMPI_VERSION=4.1.3
ARG OPENMPI_TMP=/tmp/openmpi
ARG OPENMPI_MAJOR_VERSION=4.1

ENV MPIRUN_BIN=mpirun

# Download, build, and install Open MPI.
RUN mkdir ${OPENMPI_TMP}
WORKDIR ${OPENMPI_TMP}
RUN wget https://download.open-mpi.org/release/open-mpi/v${OPENMPI_MAJOR_VERSION}/openmpi-${OPENMPI_VERSION}.tar.gz && \
    tar -xzf openmpi-${OPENMPI_VERSION}.tar.gz --directory . --strip-components 1 && \
    ./configure --prefix=${OPENMPI_HOME} && \
    make all && \
    make install && \
    rm -rf ${OPENMPI_TMP}
ENV PATH ${OPENMPI_HOME}/bin:$PATH
ENV LD_LIBRARY_PATH ${OPENMPI_HOME}/lib:$LD_LIBRARY_PATH

# Environment variables and arguments for SWAN
ENV SWAN_HOME=/swan
ARG SWAN_VERSION=4145
ARG SWAN_TMP=/tmp/swan
ENV SWAN_BIN=swan.exe

# Instal SWAN from source code
RUN mkdir ${SWAN_TMP}
WORKDIR ${SWAN_TMP}
RUN wget https://swanmodel.sourceforge.io/download/zip/swan${SWAN_VERSION}.tar.gz && \
    tar -xzf swan${SWAN_VERSION}.tar.gz --directory . --strip-components 1 && \
    make config && \
    make mpi && \
    mkdir ${SWAN_HOME} && \
    mv swan.exe swanrun ${SWAN_HOME} && \
    chmod +rx ${SWAN_HOME}/swanrun && \
    rm -rf ${SWAN_TMP}
ENV PATH ${SWAN_HOME}:$PATH

COPY --from=test_env /home /home
