FROM ubuntu:22.04 as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/schism-input-example.zip -P /home/ && \
    unzip /home/schism-input-example.zip -d /home/ && \
    rm /home/schism-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Fetch base image of ubuntu with 77 MB.
FROM ubuntu:22.04

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git wget perl cmake

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
WORKDIR /

# Install Python and pip
RUN apt-get install -y python3 python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install netcfd as required by the simulator
RUN apt-get install -y libnetcdf-dev libnetcdff-dev

# Clone the source code
RUN git clone --recurse-submodules https://github.com/schism-dev/schism.git

# Install according to the instructions
RUN cd schism && \
    mkdir build && \
    cd build && \
    rm -rf * && \
    old_line='set (OLDIO OFF CACHE BOOLEAN "Old nc output (each rank dumps its own data)")' && \
    new_line='set (OLDIO ON CACHE BOOLEAN "Old nc output (each rank dumps its own data)")' && \
    sed "s|$old_line|$new_line|" ../cmake/SCHISM.local.build > ../cmake/SCHISM.local.my_own && \
    cmake -C ../cmake/SCHISM.local.my_own -C ../cmake/SCHISM.local.ubuntu ../src/ && \
    make -j8 pschism && \
    cp bin/pschism_* bin/pschism

COPY --from=test_env /home /home
