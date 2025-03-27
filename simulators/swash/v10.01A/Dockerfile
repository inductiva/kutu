FROM python:3.11-bullseye as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/swash-input-example.zip -P /home/ && \
    unzip /home/swash-input-example.zip -d /home/ && \
    rm /home/swash-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Image with Debian bookworm doesn't work.
FROM python:3.11-bullseye

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install updates and essential tools to build and install Open MPI and SWASH.
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget ssh build-essential

# Install gcc-10 (as required by SWASH) and set it as the default GNU compiler.
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
# Open MPI has to be compiled from source because the version distributed over
# apt-get forces the use of gcc-9, which is incompatible with SWASH.
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


# Set SWASH options.
ENV SWASH_HOME=/swash
ARG SWASH_VERSION=10.01A
ARG SWASH_TMP=/tmp/swash
ENV SWASH_BIN=swash.exe

# Download, build, and install SWASH.
RUN mkdir ${SWASH_TMP}
WORKDIR ${SWASH_TMP}
RUN wget https://storage.googleapis.com/inductiva-simulators-sources/swash/v${SWASH_VERSION}/swash-${SWASH_VERSION}.tar.gz && \
    tar -xzf swash-${SWASH_VERSION}.tar.gz --directory . --strip-components 1 && \
    make config && \
    make mpi && \
    mkdir ${SWASH_HOME} && \
    mv swash.exe swashrun ${SWASH_HOME} && \
    chmod +rx ${SWASH_HOME}/swashrun && \
    sed -i '2i set -e' ${SWASH_HOME}/swashrun && \
    sed -i 's/mpirun -np \$npmpi swash.exe/mpirun -np \$npmpi -machinefile machinefile swash.exe/' ${SWASH_HOME}/swashrun && \
    rm -rf ${SWASH_TMP}
ENV PATH ${SWASH_HOME}:$PATH

COPY --from=test_env /home /home
