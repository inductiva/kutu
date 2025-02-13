# Base image
FROM ubuntu:22.04

# Arguments for version control
ARG ZLIB_VERSION=1.2.11
ARG HDF5_VERSION=1_10_5
ARG NETCDF_C_VERSION=4.7.2
ARG NETCDF_FORTRAN_VERSION=4.5.2
ARG COAWST_COMMIT=f1a4250bc64bf0c4f9d521effb47d85837c92e8a

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    BASE_DIR=/opt \
    DIR=/usr/local \
    BUILD_DIR=/opt/COAWST

# Common compiler flags
ENV CC=gcc \
    CXX=g++ \
    FC=gfortran \
    FCFLAGS="-m64 -fallow-argument-mismatch" \
    F77=gfortran \
    FFLAGS="-m64 -fallow-argument-mismatch" \
    LDFLAGS="-L$DIR/netcdf/lib -L$DIR/grib2/lib" \
    CPPFLAGS="-I$DIR/netcdf/include -I$DIR/grib2/include -fcommon"

# Install base dependencies
RUN apt-get update && apt-get install -y \
    subversion gfortran build-essential m4 gcc \
    g++ perl wget make git \
    ca-certificates gcc curl libxml2-dev libcurl4-openssl-dev cmake \
    tcsh ksh csh binutils file zlib1g-dev \
    libopenmpi-dev=4.1.2-2ubuntu1 \
    openmpi-common=4.1.2-2ubuntu1 \
    openmpi-bin=4.1.2-2ubuntu1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${BASE_DIR}


# Install zlib
RUN wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-${ZLIB_VERSION}.tar.gz && \
    tar xzvf zlib-${ZLIB_VERSION}.tar.gz && \
    cd zlib-${ZLIB_VERSION} && \
    ./configure --prefix=$DIR/grib2 && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf zlib*

# Install HDF5
RUN wget https://github.com/HDFGroup/hdf5/archive/hdf5-${HDF5_VERSION}.tar.gz && \
    tar xzvf hdf5-${HDF5_VERSION}.tar.gz && \
    cd hdf5-hdf5-${HDF5_VERSION} && \
    ./configure --prefix=$DIR/netcdf --with-zlib=$DIR/grib2 --enable-fortran --enable-shared && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf hdf5*

# Install NetCDF-C
RUN wget https://github.com/Unidata/netcdf-c/archive/v${NETCDF_C_VERSION}.tar.gz && \
    tar xzvf v${NETCDF_C_VERSION}.tar.gz && \
    cd netcdf-c-${NETCDF_C_VERSION} && \
    ./configure --prefix=$DIR/netcdf --disable-dap --enable-netcdf4 --enable-hdf5 --enable-shared && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf v${NETCDF_C_VERSION}.tar.gz netcdf-c*

# Install NetCDF-Fortran
ENV LIBS="-lnetcdf -lz"
RUN wget https://github.com/Unidata/netcdf-fortran/archive/v${NETCDF_FORTRAN_VERSION}.tar.gz && \
    tar xzvf v${NETCDF_FORTRAN_VERSION}.tar.gz && \
    cd netcdf-fortran-${NETCDF_FORTRAN_VERSION} && \
    ./configure --prefix=$DIR/netcdf --disable-hdf5 --enable-shared && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf netcdf-fortran* v${NETCDF_FORTRAN_VERSION}.tar.gz


# COAWST environment setup
ENV MCT_INCDIR=/opt/COAWST/Lib/MCT/include \
    MCT_LIBDIR=/opt/COAWST/Lib/MCT/lib \
    MCT_DIR=${BASE_DIR}/COAWST/Lib/MCT \
    COAWST_DIR=/opt/COAWST \
    NETCDF=/usr/local/netcdf \
    NETCDF_CONFIG=/usr/local/netcdf/bin/nc-config \
    FCFLAGS="${FCFLAGS}-ffree-form -ffree-line-length-none -fconvert=big-endian -frecord-marker=4 -fallow-argument-mismatch -fallow-invalid-boz" \
    FFLAGS="$FCFLAGS" \
    MY_ROOT_DIR=/opt/COAWST \
    MY_PROJECT_DIR=/opt/COAWST \
    USE_MPI=ON \
    USE_MPIF90=ON \
    FORT=gfortran \
    CC=gcc \
    CXX=g++ \
    FC=gfortran \
    WWATCH3_NETCDF=NC4 \
    NETCDF4=1 \
    WRFIO_NCD_LARGE_FILE_SUPPORT=1 \
    LD_LIBRARY_PATH=$DIR/netcdf/lib:$DIR/grib2/lib:${LD_LIBRARY_PATH} \
    PATH=$DIR/netcdf/bin:${COAWST_DIR}:/workdir/output/artifacts/__COAWST:${PATH} \
    JASPERLIB=$DIR/grib2/lib \
    JASPERINC=$DIR/grib2/include \
    HDF5=$DIR/netcdf \
    COMMON_FLAGS="-O2 -fPIC -fno-strict-aliasing -fno-lto -w"\
    MY_CPP_FLAGS="-DDUCKNC"




# Clone and setup COAWST
RUN cd ${BASE_DIR} && \
    git clone https://github.com/DOI-USGS/COAWST.git && \
    cd COAWST && \
    git checkout ${COAWST_COMMIT}

    


# Build SCRIP_COAWST
RUN cd ${COAWST_DIR}/Lib/SCRIP_COAWST && \
    sed -i -e 's/FORT = .*/FORT = gfortran/' \
           -e 's/FC = .*/FC = gfortran/' \
           -e "s/FCFLAGS = .*/FCFLAGS = ${COMMON_FLAGS}/" \
           -e 's/LDFLAGS = .*/LDFLAGS = -fno-strict-aliasing -fno-lto -w/' \
           -e 's/USE_MPI=.*/USE_MPI=on/' \
           -e 's/USE_MPIF90=.*/USE_MPIF90=on/' \
           makefile && \
    make -j1 >coawst_make.txt 2>&1

RUN cd $MCT_DIR && \
    ./configure FC=mpif90  FCFLAGS="-O2 -fPIC -frecord-marker=4 -fconvert=big-endian -fallow-argument-mismatch" \
    -prefix=${MCT_DIR} &&\
    make >mct_make.txt 2>&1 && \
    make install >mct_make_install.txt 2>&1

COPY /build_coawst_inlet_refined.sh /opt/COAWST/build_coawst_inlet_refined.sh

# Configure COAWST build environment for INLET_TEST Refined
RUN cd ${COAWST_DIR} && \
    chmod +x build_coawst_inlet_refined.sh && \
    mkdir -p Build_roms 

# Compile the application with parallel processing
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inlet_refined.sh -j $(nproc)

# Rename the executable
RUN cp ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_roms_swan_redefined_grid

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh


COPY /functions/create_all_sim_links /usr/bin/create_all_sim_links

RUN chmod +x /usr/bin/create_all_sim_links
