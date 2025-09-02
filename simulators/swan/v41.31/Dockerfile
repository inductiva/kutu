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
ARG OPENMPI_VERSION=4.0.1
ARG OPENMPI_TMP=/tmp/openmpi
ARG OPENMPI_MAJOR_VERSION=4.0

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
ENV UNSWAN_HOME=/unswan
ARG SWAN_VERSION=41.31
ARG SWAN_TMP=/tmp/swan
ENV SWAN_BIN=swan.exe
ENV Metis_ROOT=/usr

# install gklib and metis (needed for unstructured swan)
RUN cd / && \
    git clone https://github.com/KarypisLab/GKlib.git && \
    cd GKlib && \
    make config cc=mpicc prefix=/usr && \
    make && \
    make install && \
    cd / && \
    git clone https://github.com/KarypisLab/METIS.git && \
    cd METIS && \
    make config shared=1 cc=mpicc prefix=/usr && \
    make install

# Instal SWAN from source code
RUN mkdir ${SWAN_TMP}
WORKDIR ${SWAN_TMP}

ENV FLAGS_MSC ="-W0 -assume byterecl -traceback -diag-disable 8290 -diag-disable 8291 -diag-disable 8293"

# compile swan -> with mpi and strucutured
RUN wget https://storage.googleapis.com/inductiva-simulators-sources/swan/v${SWAN_VERSION}/swan${SWAN_VERSION}.tar.gz && \
    tar -xzf swan${SWAN_VERSION}.tar.gz --directory . --strip-components 1 && \
    make config && \
    make mpi FLAGS_OPT="-g -fallow-argument-mismatch" && \
    mkdir ${SWAN_HOME} && \
    mv swan.exe swanrun ${SWAN_HOME} && \
    chmod +rx ${SWAN_HOME}/swanrun && \
    rm -rf ${SWAN_TMP} && \
    sed -i '2i set -e' ${SWAN_HOME}/swanrun && \
    sed -i 's/mpirun -np \$npmpi swan.exe/mpirun -np \$npmpi -machinefile machinefile swan.exe/' ${SWAN_HOME}/swanrun

# compile swan -> with openmp and unstructured
RUN wget https://storage.googleapis.com/inductiva-simulators-sources/swan/v${SWAN_VERSION}/swan${SWAN_VERSION}.tar.gz && \
    tar -xzf swan${SWAN_VERSION}.tar.gz --directory . --strip-components 1 && \
    mkdir build ${UNSWAN_HOME} && \
    cd build && \
    cmake .. \
        -DMETIS=ON \
        -DOPENMP=ON \
        -DCMAKE_C_COMPILER=mpicc \
        -DCMAKE_CXX_COMPILER=mpicxx \
        -DCMAKE_Fortran_COMPILER=mpif90 \
        -DNETCDF=ON \
        -DCMAKE_INSTALL_PREFIX=${UNSWAN_HOME} && \
    make && \
    make install && \
    mv bin/swan.exe bin/unswan.exe && \
    mv ../bin/swanrun ../bin/unswanrun && \
    cp bin/unswan.exe ../bin/unswanrun ${UNSWAN_HOME} && \
    chmod +rx ${UNSWAN_HOME}/unswanrun && \
    rm -rf ${SWAN_TMP} && \
    sed -i '2i set -e' ${UNSWAN_HOME}/unswanrun && \
    sed -i 's/swan\.exe/unswan.exe/g' ${UNSWAN_HOME}/unswanrun

ENV PATH ${SWAN_HOME}:${UNSWAN_HOME}:$PATH

COPY --from=test_env /home /home
