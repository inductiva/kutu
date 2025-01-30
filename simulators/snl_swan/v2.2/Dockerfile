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
ARG OPENMPI_VERSION=4.0.1
ARG OPENMPI_TMP=/tmp/openmpi
ARG OPENMPI_MAJOR_VERSION=4.0

ENV MPIRUN_BIN=mpirun \
    OMPI_ALLOW_RUN_AS_ROOT=1\
    OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

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
ENV SWAN_HOME=/home
ARG SWAN_VERSION=2.2
ARG SWAN_TMP=/tmp/swan
ARG SWAN_EXAMPLES=/home/snl-input-example

ENV SWAN_BIN=swan.exe

# Instal SWAN from source code
RUN mkdir -p ${SWAN_TMP} ${SWAN_EXAMPLES}
WORKDIR ${SWAN_TMP}

ENV FLAGS_MSC ="-W0 -assume byterecl -traceback -diag-disable 8290 -diag-disable 8291 -diag-disable 8293"



# Install SWAN from source code
RUN wget https://github.com/sandialabs/SNL-SWAN/archive/refs/tags/v${SWAN_VERSION}.tar.gz && \
    tar -xzf v${SWAN_VERSION}.tar.gz --directory . --strip-components 1 && \
    cd src &&\
    perl platform.pl && \
    make mpi FLAGS_OPT="-g -fallow-argument-mismatch" > build.log |tee build.log && \
    mkdir -p ${SWAN_HOME} && \
    mv ../tutorial ${SWAN_HOME} &&\
    mv swan.exe hcat.exe swanrun /bin && \
    chmod +rx /bin/swanrun 


COPY /INPUT ${SWAN_HOME}/tutorial




COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh





WORKDIR ${SWAN_HOME}/tutorial


# Default command (can be overridden)
CMD ["swan.exe"]