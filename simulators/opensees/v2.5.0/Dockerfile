# Base image with common build dependencies
FROM ubuntu:14.04 AS base
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/src
ENV CXXFLAGS="-fpermissive"

# Build arguments and versions
ARG OPENSEES_VERSION=v2.5.0
# System dependencies
RUN apt-get update && apt-get install -y \
    tcl8.5-dev \
    tcl8.5 \
    tk8.5-dev \
    cmake \
    gcc \
    g++ \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libopenblas-dev \
    libarpack2-dev \
    libparpack2-dev \
    libarpack++2-dev \
    libsuitesparse-dev \
    #MUMPS
    libmumps-dev \
    libmumps-scotch-dev \
    python3-pip \
    libopenmpi-dev \
    openmpi-common \
    libmumps-dev \
    wget \
    && rm -rf /var/lib/apt/lists/* && \
    mkdir /src && \
    mkdir /src/lib && \
    mkdir /src/bin

# Download and extract OpenSees source
WORKDIR /src
RUN mkdir /scalapack && \
    cd /scalapack && \
    wget http://www.netlib.org/scalapack/scalapack-2.0.2.tgz && \
    tar -xvzf scalapack-2.0.2.tgz && \
    cd scalapack-2.0.2 && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr .. && \
    make -j && \
    make install && \
    mkdir /blacs && \
    cd /blacs/ && \
    wget http://www.netlib.org/blacs/mpiblacs.tgz && \
    tar -xzvf mpiblacs.tgz && \
    cd BLACS && \
    cp BMAKES/Bmake.MPI-LINUX Bmake.inc && \
    sed -i 's|BTOPdir = $(HOME)/BLACS|BTOPdir = /blacs/BLACS|' Bmake.inc && \
    sed -i 's|MPIdir = /usr/local/mpich|MPIdir = /usr/lib/openmpi|' Bmake.inc && \
    sed -i 's|   F77            = g77|   F77            = gfortran|' Bmake.inc && \
    sed -i 's|   F77NO_OPTFLAGS =|   F77NO_OPTFLAGS = -I/usr/lib/openmpi/include/|' Bmake.inc && \
    make mpi && \
    cp /blacs/BLACS/LIB/blacs_MPI-LINUX-0.a /src/lib/blacs_MPI-LINUX-0.a && \
    cp /blacs/BLACS/LIB/blacsCinit_MPI-LINUX-0.a /src/lib/blacsCinit_MPI-LINUX-0.a && \
    cp /blacs/BLACS/SRC/MPI/INTERNAL/bi_f77_get_constants.o /src/lib/bi_f77_get_constants.o && \
    cp /blacs/BLACS/LIB/blacsF77init_MPI-LINUX-0.a /src/lib/blacsF77init_MPI-LINUX-0.a && \
    mkdir /lapack && \
    cd /lapack && \
    wget http://www.netlib.org/lapack/lapack-lite-3.1.0.tgz && \
    tar -xzvf lapack-lite-3.1.0.tgz && \
    cd lapack-3.1.0 && \
    mv make.inc.example make.inc && \
    sed -i 's|FORTRAN  = g77|FORTRAN  = gfortran|' make.inc && \
    sed -i 's|LOADER   = g77|LOADER   = gfortran|' make.inc && \
    cd BLAS/SRC && \
    make && \
    cp /lapack/lapack-3.1.0/blas_LINUX.a /src/lib/blas_LINUX.a && \
    cd /src && \
    wget https://github.com/OpenSees/OpenSees/archive/refs/tags/${OPENSEES_VERSION}.tar.gz \
    && tar xzf ${OPENSEES_VERSION}.tar.gz \
    && rm ${OPENSEES_VERSION}.tar.gz \
    && mv OpenSees-* OpenSees && \
    cd OpenSees && \
    cp MAKES/Makefile.def.OPENMPI . && \
    mv MAKES/Makefile.def.OPENMPI Makefile.def && \
    sed -i 's|TCL_INCLUDES = -I/usr/includes/tcl-private/generic|TCL_INCLUDES = -I/usr/include/tcl8.5/tcl-private/generic|' Makefile.def && \
    sed -i 's|SUPERLUdir   = $(HOME)/OpenSees/OTHER/SuperLU_4.1/SRC|SUPERLUdir   = $(HOME)/OpenSees/OTHER/SuperLU_5.0/SRC|' Makefile.def && \
    sed -i 's|TCL_LIBRARY = /usr/lib64/libtcl8.5.so|TCL_LIBRARY = /usr/lib/x86_64-linux-gnu/libtcl8.5.so|' Makefile.def && \
    sed -i 's|$(HOME)/lib/libdmumps.a \\|/usr/lib/libdmumps.a \\|' Makefile.def && \
    sed -i 's|$(HOME)/lib/libmumps_common.a \\|/usr/lib/libmumps_common.a \\|' Makefile.def && \
    sed -i 's|$(HOME)/lib/libpord.a \\|/usr/lib/libpord.a \\|' Makefile.def && \
    sed -i 's|        $(HOME)/lib/libscalapack.a \\|        /usr/lib/libscalapack.a \\|' Makefile.def && \
    sed -i 's|$(HOME)/PARALLEL_NUMERICAL_LIBS/BLACS/SRC/MPI/INTERNAL/bi_f77_get_constants.o|/src/lib/bi_f77_get_constants.o|' Makefile.def && \
    sed -i 's|LINKFLAGS       = -rdynamic -Wl|LINKFLAGS       = -rdynamic|' Makefile.def && \
    cd OTHER/SuperLU_DIST_2.5/SRC/ && \
    make && \
    cd /src/OpenSees/ && \
    make

RUN mkdir /home/opensees-input-example && \
    cp /src/OpenSees/EXAMPLES/verification/PlanarTruss.tcl /home/opensees-input-example/PlanarTruss.tcl


ENV PATH="/src/bin:${PATH}"

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh
