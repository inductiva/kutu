# Stage 1: Test Environment
FROM ubuntu:22.04 AS test_env
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up directories for examples and output
RUN mkdir -p /home/seissol/examples /home/seissol/output

# Clone SeisSol examples repository
RUN git clone https://github.com/SeisSol/Examples.git /home/seissol/examples

# Download specific test data for tpv33 example
WORKDIR /home/seissol/examples/tpv33
RUN wget https://zenodo.org/record/8042664/files/tpv33_half_sym.xdmf -O tpv33_half_sym.xdmf \
    && wget https://zenodo.org/record/8042664/files/tpv33_half_sym -O tpv33_half_sym


# Stage 2: Build Environment
FROM ubuntu:22.04 AS build

# Consolidated environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    SEISSOL_COMMTHREAD=0 \
    SEISSOL_PREFIX=/usr/local \
    PATH="/SeisSol/build:$PATH" \
    BUILD_DEPS="build-essential cmake git wget openmpi-bin libopenmpi-dev gfortran libhdf5-dev \
                libnetcdf-dev libnetcdf-mpi-dev libblas-dev liblapack-dev python3 python3-pip \
                tzdata unzip lua5.3 liblua5.3-dev nano zlib1g-dev" \
    CC=mpicc \
    CXX=mpicxx \
    FC=mpif90 \
    CFLAGS="-fPIC" \
    CXXFLAGS="-fPIC" \
    FFLAGS="-fPIC" \
    MPI_DIR=/usr/lib/x86_64-linux-gnu/openmpi \
    HDF5_DIR=/usr/local \
    HDF5_INCLUDE_DIR=/usr/include/hdf5/parallel

# Update system and install essential tools
RUN apt-get update && apt-get install -y ${BUILD_DEPS} && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Common CMake flags for all builds
ENV CMAKE_COMMON_FLAGS="-DCMAKE_INSTALL_PREFIX=${SEISSOL_PREFIX} \
                       -DCMAKE_C_COMPILER=${CC} \
                       -DCMAKE_CXX_COMPILER=${CXX} \
                       -DCMAKE_Fortran_COMPILER=${FC}"

#    Update system and install essential tools
RUN apt-get update && apt-get install -y ${BUILD_DEPS} && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set timezone to UTC
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# Install Python dependencies
RUN pip3 install numpy setuptools jupyterlab

# Copy test environment data
COPY --from=test_env /home/seissol/examples /home/seissol/examples

# Install Eigen
RUN wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz && \
    tar -xf eigen-3.4.0.tar.gz && \
    cd eigen-3.4.0 && \
    mkdir build && cd build && \
    cmake .. ${CMAKE_COMMON_FLAGS} && \
    make install && \
    cd ../.. && rm -rf eigen-3.4.0*



# Install ParMETIS
RUN wget https://ftp.mcs.anl.gov/pub/pdetools/spack-pkgs/parmetis-4.0.3.tar.gz && \
    tar -xvf parmetis-4.0.3.tar.gz && \
    cd parmetis-4.0.3 && \
    sed -i 's/IDXTYPEWIDTH 32/IDXTYPEWIDTH 64/g' ./metis/include/metis.h && \
    make config cc=mpicc cxx=mpicxx prefix=${SEISSOL_PREFIX} && \
    make install && \
    cp build/Linux-x86_64/libmetis/libmetis.a ${SEISSOL_PREFIX}/lib && \
    cp metis/include/metis.h ${SEISSOL_PREFIX}/include && \
    cd .. && rm -rf parmetis-4.0.3*

# Install yaml-cpp
RUN git clone https://github.com/jbeder/yaml-cpp.git /yaml-cpp && \
    cd /yaml-cpp && \
    mkdir build && cd build && \
    cmake .. -DYAML_BUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=${SEISSOL_PREFIX} && \
    make -j$(nproc) && make install && \
    cd ../.. && rm -rf /yaml-cpp

# Install HDF5 with MPI support
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.3/src/hdf5-1.12.3.tar.bz2 && \
    tar -xaf hdf5-1.12.3.tar.bz2 && \
    cd hdf5-1.12.3 && \
    CPPFLAGS="-fPIC ${CPPFLAGS}" \
    CC=mpicc CXX=mpicxx \
    ./configure \
        --enable-parallel \
        --prefix=/usr/local \
        --with-zlib \
        --enable-shared \
        --enable-static \
        --with-mpi=/usr/lib/x86_64-linux-gnu/openmpi \
        --includedir=/usr/include/hdf5/parallel && \
        make -j$(nproc) && make install && \
    cd .. && rm -rf hdf5-1.12.3*

# Install ImpalaJIT
RUN git clone https://github.com/uphoffc/ImpalaJIT.git /ImpalaJIT && \
    cd /ImpalaJIT && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=${SEISSOL_PREFIX} && \
    make -j$(nproc) && make install && \
    cd ../.. && rm -rf /ImpalaJIT

# Install NetCDF with Parallel I/O
RUN wget https://downloads.unidata.ucar.edu/netcdf-c/4.8.1/netcdf-c-4.8.1.tar.gz && \
    tar -xaf netcdf-c-4.8.1.tar.gz && \
    cd netcdf-c-4.8.1 && \
    CFLAGS="-fPIC ${CFLAGS}" CC=h5pcc ./configure --enable-shared=no --prefix=${SEISSOL_PREFIX} --disable-dap && \
    make -j$(nproc) && make install && \
    cd .. && rm -rf netcdf-c-4.8.1*

# Install libxsmm gemm generator
RUN git clone --depth=1 --branch 1.17 https://github.com/hfp/libxsmm && \
    cd libxsmm && \
    make generator && \
    cp bin/libxsmm_gemm_generator ${SEISSOL_PREFIX}/bin/ && \
    cd .. && rm -rf libxsmm


# Install ASAGI
RUN git clone https://github.com/TUM-I5/ASAGI.git /asagi && \
    cd /asagi && \
    git submodule update --init && \
    mkdir build && cd build && \
    cmake .. ${CMAKE_COMMON_FLAGS}  \
    -DSHARED_LIB=ON \
    -DSTATIC_LIB=ON \
    -DUSE_MPI=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=${SEISSOL_PREFIX} \
    -DCMAKE_INCLUDE_PATH=${SEISSOL_PREFIX}/include \
    -DCMAKE_LIBRARY_PATH=${SEISSOL_PREFIX}/lib && \
        make -j$(nproc) && make install && \
        cd ../.. && rm -rf /asagi


# Install EASI
RUN git clone --recursive https://github.com/SeisSol/easi.git /easi && \
    cd /easi && \
    mkdir build && cd build && \
    cmake .. ${CMAKE_COMMON_FLAGS} -DCMAKE_PREFIX_PATH=${SEISSOL_PREFIX} -DASAGI=ON -DIMPALAJIT=ON -DLUA=ON \
    -DUSE_MPI=ON && \
    make -j$(nproc) && make install && \
    cd ../.. && rm -rf /easi



# Clone SeisSol with submodules and check out 5d88567c8733937b99d47ea00b0f26b8bf467785 commit
RUN git clone --recursive https://github.com/SeisSol/SeisSol.git /SeisSol && \
    cd /SeisSol && \
    git checkout 5d88567c8733937b99d47ea00b0f26b8bf467785 && \
    git submodule update --init --recursive

# modify the namespace resolution
RUN sed -i 's/asagiReader = std::make_unique<seissol::asagi::AsagiReader>("SEISSOL_ASAGI");/asagiReader = std::make_unique<easi::AsagiReader>();/g' /SeisSol/src/Initializer/InitialFieldProjection.cpp
RUN sed -i 's/const auto dimensionNames = \(.*\)/std::set<std::string> dimensionNames = \1/g' /SeisSol/src/Initializer/InitialFieldProjection.cpp
# Build SeisSol
WORKDIR /SeisSol
RUN mkdir -p build && cd build && \
cmake .. ${CMAKE_COMMON_FLAGS} \
    -DNUMA_AWARE_PINNING=ON \
    -DASAGI=ON \
    -DASAGI_NAMESPACE=easi \
    -DASAGI_ROOT=${SEISSOL_PREFIX} \
    -DEASI=ON \
    -DPRECISION=double \
    -DORDER=4 \
    -DEQUATIONS=elastic \
    -DHDF5_PARALLEL=ON \
    -DHDF5_ROOT=${HDF5_DIR} \
    -DHDF5_INCLUDE_DIRS=${HDF5_INCLUDE_DIR} \
    -DUSE_MPI=ON \
    -DUSE_OPENMP=ON \
    -DUSE_HDF5=ON \
    -DHDF5_PREFER_PARALLEL=ON \
    -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc)
# Prepare test environment
WORKDIR /home/seissol/examples/tpv33

# Copy test simulation script
COPY ./test_sim.sh /home/seissol/examples/tpv33/test_sim.sh
RUN chmod +x /home/seissol/examples/tpv33/test_sim.sh

# Expose Jupyter port
EXPOSE 53155

# Default command to run the test script
CMD ["/home/seissol/examples/tpv33/test_sim.sh"]
