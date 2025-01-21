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
    && rm -rf /var/lib/apt/lists/*

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

# Install MPICH
RUN wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/mpich-3.0.4.tar.gz && \
    tar xzvf mpich-3.0.4.tar.gz && \
    cd mpich-3.0.4 && \
    ./configure --prefix=$DIR/mpich && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf mpich*


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
    MPICH_F90=gfortran \
    MPICH_FC=gfortran \
    FORT=gfortran \
    CC=gcc \
    CXX=g++ \
    FC=gfortran \
    WWATCH3_NETCDF=NC4 \
    NETCDF4=1 \
    WRFIO_NCD_LARGE_FILE_SUPPORT=1 \
    LD_LIBRARY_PATH=$DIR/netcdf/lib:$DIR/grib2/lib:$DIR/mpich/lib \
    PATH=$DIR/netcdf/bin:$DIR/mpich/bin:${PATH} \
    JASPERLIB=$DIR/grib2/lib \
    JASPERINC=$DIR/grib2/include \
    MPI_ROOT=$DIR/mpich \
    MPI_INCLUDE=$DIR/mpich/include \
    HDF5=$DIR/netcdf \
    MPI_LIB=$DIR/mpich/lib\
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
    make -j1

RUN cd $MCT_DIR && \
    ./configure FC=mpif90  FCFLAGS="-O2 -fPIC -frecord-marker=4 -fconvert=big-endian" \
    -prefix=${MCT_DIR} &&\
    make && \
    make install 

# Configure COAWST build environment
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_ducknc.sh && \
    chmod +x build_coawst_ducknc.sh && \
    mkdir -p Build_roms && \
    sed -i -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
           -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
           -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
           -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
           -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
           -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
           -e "s|export\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|"  \
           -e "s|export\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=${MY_ROOT_DIR}|"  \
           -e "s|export\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=${MY_PROJECT_DIR}/Projects/Ducknc|"  \
           -e "s|export\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=${MY_PROJECT_DIR}/Projects/Ducknc|"  \
           -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=Ducknc|" \
           -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=DUCKNC|" \
           build_coawst_ducknc.sh && \
    echo "export WRF_EM_CORE=1" >> build_coawst_ducknc.sh && \
    echo "export NETCDF4=1" >> build_coawst_ducknc.sh && \
    echo "export WRFIO_NCD_LARGE_FILE_SUPPORT=1" >> build_coawst_ducknc.sh 

RUN cd ${COAWST_DIR} && \
    ./build_coawst_ducknc.sh -j $(nproc)

RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Ducknc

RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_estuary.sh && \
    chmod +x build_coawst_estuary.sh && \
    mkdir -p Build_roms && \
    sed -i -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Estuary_test2|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Estuary_test2|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=ESTUARY_TEST2|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=ESTUARY_TEST2|" \
    build_coawst_estuary.sh && \
    echo "export NETCDF4=1" >> build_coawst_estuary.sh 
RUN cd ${COAWST_DIR} && \
    ./build_coawst_estuary.sh -j $(nproc)
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Estuary_test2

# Configure COAWST build environment for INLET_TEST
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inlet.sh && \
    chmod +x build_coawst_inlet.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/Coupled|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/Coupled|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=INLET_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=INLET_TEST|" \
    build_coawst_inlet.sh && \
    echo "export NETCDF4=1" >> build_coawst_inlet.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inlet.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test

# Configure COAWST build environment for INLET_TEST DiffGrid
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inlet_diffgrid.sh && \
    chmod +x build_coawst_inlet_diffgrid.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/DiffGrid|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/DiffGrid|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=INLET_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=INLET_TEST|" \
    build_coawst_inlet_diffgrid.sh && \
    echo "export NETCDF4=1" >> build_coawst_inlet_diffgrid.sh && \
    # Ensure MCT interpolation is enabled
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DMCT_INTERP_OC2WV\"" >> build_coawst_inlet_diffgrid.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inlet_diffgrid.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test_diffgrid

# Configure COAWST build environment for INLET_TEST InWave
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inlet_inwave.sh && \
    chmod +x build_coawst_inlet_inwave.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/InWave|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/InWave|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=INLET_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=INLET_TEST|" \
    build_coawst_inlet_inwave.sh && \
    echo "export NETCDF4=1" >> build_coawst_inlet_inwave.sh && \
    # Add InWave model specific flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DINWAVE_MODEL\"" >> build_coawst_inlet_inwave.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inlet_inwave.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test_inwave

# Configure COAWST build environment for INLET_TEST Refined
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inlet_refined.sh && \
    chmod +x build_coawst_inlet_refined.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/Refined|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/Refined|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=INLET_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=INLET_TEST|" \
    build_coawst_inlet_refined.sh && \
    echo "export NETCDF4=1" >> build_coawst_inlet_refined.sh && \
    # Add refinement specific flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DREFINEMENT\"" >> build_coawst_inlet_refined.sh

# Compile the application with parallel processing
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inlet_refined.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test_refined

# Configure COAWST build environment for INLET_TEST Swanonly
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inlet_swanonly.sh && \
    chmod +x build_coawst_inlet_swanonly.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/Swanonly|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Inlet_test/Swanonly|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=INLET_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=INLET_TEST|" \
    build_coawst_inlet_swanonly.sh && \
    echo "export NETCDF4=1" >> build_coawst_inlet_swanonly.sh && \
    # Add SWAN model flag
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DSWAN_MODEL\"" >> build_coawst_inlet_swanonly.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inlet_swanonly.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test_swanonly

# Configure COAWST build environment for InWave_shoreface
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inwave_shoreface.sh && \
    chmod +x build_coawst_inwave_shoreface.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/InWave_shoreface|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/InWave_shoreface|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=INWAVE_SHOREFACE|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=INWAVE_SHOREFACE|" \
    build_coawst_inwave_shoreface.sh && \
    echo "export NETCDF4=1" >> build_coawst_inwave_shoreface.sh && \
    # Add InWave model flag and ensure SWAN coupling is disabled
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DINWAVE_MODEL\"" >> build_coawst_inwave_shoreface.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_inwave_shoreface.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_inwave_shoreface




# Configure COAWST build environment for JOE_TC Coupled
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_joe_tc.sh && \
    chmod +x build_coawst_joe_tc.sh && \
    mkdir -p Build_roms && \
    # Copy WRF input files to root directory
    cp Projects/JOE_TC/wrfbdy_d01 . && \
    cp Projects/JOE_TC/wrfinput_d01 . && \
    cp Projects/JOE_TC/namelist.input . && \
    sed -i \
    -e 's/nproc_x                             = 1/nproc_x                             = 2/' \
    -e 's/nproc_y                             = 1/nproc_y                             = 2/' \
    namelist.input &&\
    sed -i \
    -e 's/NnodesATM\s*=\s*1/NnodesATM = 4/' \
    -e 's/NnodesWAV\s*=\s*1/NnodesWAV = 4/' \
    -e 's/NnodesOCN\s*=\s*1/NnodesOCN = 4/' \
    -e 's/TI_ATM2WAV\s*=.*$/TI_ATM_WAV = 600.0d0/' \
    -e 's/TI_ATM2OCN\s*=.*$/TI_ATM_OCN = 600.0d0/' \
    -e 's/TI_WAV2OCN\s*=.*$/TI_WAV_OCN = 600.0d0/' \
    -e "s|ATM_name\s*=.*$|ATM_name = namelist.input|" \
    -e "s|WAV_name\s*=.*$|WAV_name = Projects/JOE_TCs/INPUT_JOE_TC|" \
    -e "s|OCN_name\s*=.*$|OCN_name = Projects/JOE_TCs/ocean_joe_tc.in|" \
    Projects/JOE_TC/Coupled/coupling_joe_tc.in && \
    # Update ocean file for tile partitioning
    sed -i \
    -e 's/NtileI == 1/NtileI == 4/' \
    -e 's/NtileJ == 1/NtileJ == 3/' \
    Projects/JOE_TC/Coupled/ocean_joe_tc.in && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/JOE_TC/Coupled|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/JOE_TC/Coupled|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=JOE_TC|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=JOE_TC|" \
    build_coawst_joe_tc.sh && \
    # Add required environment variables
    echo "NETCDF_classic=1" >> build_coawst_joe_tc.sh && \
    echo "export PNETCDF=\"\"" >> build_coawst_joe_tc.sh && \
    # Add model flags for three-way coupling
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSWAN_MODEL -DWRF_MODEL\"" >> build_coawst_joe_tc.sh


# Compile the application
RUN cd ${COAWST_DIR} && \
    printf '34\n1\n'| ./build_coawst_joe_tc.sh -j $(nproc)

RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_joe_tc

RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_ripcurrent.sh && \
    chmod +x build_coawst_ripcurrent.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Rip_current|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Rip_current|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=RIP_CURRENT|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=RIP_CURRENT|" \
    build_coawst_ripcurrent.sh && \
    echo "export NETCDF4=1" >> build_coawst_ripcurrent.sh && \
    # Add required flags for coupled ROMS+SWAN
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSWAN_MODEL\"" >> build_coawst_ripcurrent.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_ripcurrent.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_ripcurrent

RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_sedbed.sh && \
    chmod +x build_coawst_sedbed.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Sed_bed_toy|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Sed_bed_toy|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=SED_BED_TOY|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=SED_BED_TOY|" \
    build_coawst_sedbed.sh && \
    echo "export NETCDF4=1" >> build_coawst_sedbed.sh && \
    # Add sediment module flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSEDIMENT\"" >> build_coawst_sedbed.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_sedbed.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_sedbed.sh

RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_trench.sh && \
    chmod +x build_coawst_trench.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Trench|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Trench|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=TRENCH|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=TRENCH|" \
    build_coawst_trench.sh && \
    echo "export NETCDF4=1" >> build_coawst_trench.sh && \
    # Add sediment morphology flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSEDIMENT -DMORPHOLOGY\"" >> build_coawst_trench.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_trench.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_trench.sh

RUN cd ${COAWST_DIR} && \
    cp Projects/wetdry/wetdry_slope_chan.h Projects/wetdry/wetdry.h &&\
    cp build_coawst.sh build_coawst_wetdry.sh && \
    chmod +x build_coawst_wetdry.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/wetdry|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/wetdry|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=WETDRY|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=WETDRY|" \
    build_coawst_wetdry.sh && \
    echo "export NETCDF4=1" >> build_coawst_wetdry.sh && \
    # Add wetting/drying flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DWETDRY\"" >> build_coawst_wetdry.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_wetdry.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_wetdry.sh

RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_Sed_floc_toy.sh && \
    chmod +x build_coawst_Sed_floc_toy.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Sed_floc_toy|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Sed_floc_toy|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=SED_FLOC_TOY|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=SED_FLOC_TOY|" \
    build_coawst_Sed_floc_toy.sh && \
    echo "export NETCDF4=1" >> build_coawst_Sed_floc_toy.sh && \
    # Add sediment and biogeochemistry flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSEDIMENT -DBIO_SEDIMENT\"" >> build_coawst_Sed_floc_toy.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_Sed_floc_toy.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Sed_floc_toy.sh

RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_vegrowth.sh && \
    chmod +x build_coawst_vegrowth.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Veg_growth_test|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Veg_growth_test|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=VEG_GROWTH_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=VEG_GROWTH_TEST|" \
    build_coawst_vegrowth.sh && \
    echo "export NETCDF4=1" >> build_coawst_vegrowth.sh && \
    # Add all required module flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSEDIMENT -DBIO_FENNEL -DESTUARYBGC -DVEGETATION -DSPECTRAL_LIGHT\"" >> build_coawst_vegrowth.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_vegrowth.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_vegrowth.sh


RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_marsh.sh && \
    chmod +x build_coawst_marsh.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/Veg_test|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/Veg_test|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=VEG_TEST|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=VEG_TEST|" \
    build_coawst_marsh.sh && \
    echo "export NETCDF4=1" >> build_coawst_marsh.sh && \
    # Add marsh dynamics and required module flags
    echo "export MY_CPP_FLAGS=\"\${MY_CPP_FLAGS} -DROMS_MODEL -DSEDIMENT -DVEGETATION -DMARSH_DYNAMICS -DWAVE_THRUST_MARSH -DMARSH_BIOMASS\"" >> build_coawst_marsh.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
    ./build_coawst_marsh.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_marsh.sh

# Configure COAWST build environment for JOE_TC DiffGrid
RUN cd ${COAWST_DIR} && \
    cp /opt/COAWST/Projects/JOE_TC/DiffGrid/joe_tc.h /opt/COAWST/Projects/JOE_TC/DiffGrid/joe_tc_diffgrid.h &&\
    cp build_coawst.sh build_coawst_joetc_diffgrid.sh && \
    chmod +x build_coawst_joetc_diffgrid.sh && \
    mkdir -p Build_roms && \
    sed -i \
    -e 's/\$cmd_wrf/#\$cmd_wrf/g' \
    -e "s/-O2 -fPIC/${COMMON_FLAGS}/g" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=${COAWST_DIR}|" \
    -e "s|export\\s*FORT=.*|export FORT=gfortran|" \
    -e "s|export\\s*USE_MPI=.*|export USE_MPI=on|" \
    -e "s|export\\s*USE_MPIF90=.*|export USE_MPIF90=on|" \
    -e "s|export\\s*MY_ROOT_DIR=.*|export MY_ROOT_DIR=/opt/COAWST|" \
    -e "s|export\\s*MY_PROJECT_DIR=.*|export MY_PROJECT_DIR=\${MY_ROOT_DIR}|" \
    -e "s|export\\s*MY_HEADER_DIR=.*|export MY_HEADER_DIR=\${MY_PROJECT_DIR}/Projects/JOE_TC/DiffGrid|" \
    -e "s|export\\s*MY_ANALYTICAL_DIR=.*|export MY_ANALYTICAL_DIR=\${MY_PROJECT_DIR}/Projects/JOE_TC/DiffGrid|" \
    -e "s|export\\s*COAWST_APPLICATION=.*|export COAWST_APPLICATION=JOE_TC_DIFFGRID|" \
    -e "s|export\\s*ROMS_APPLICATION=.*|export ROMS_APPLICATION=JOE_TC_DIFFGRID|" \
    build_coawst_joetc_diffgrid.sh && \
    echo "export NETCDF4=1" >> build_coawst_joetc_diffgrid.sh

# Compile the application
RUN cd ${COAWST_DIR} && \
printf '34\n1\n' | ./build_coawst_joetc_diffgrid.sh -j $(nproc)

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_joetc_diffgrid

WORKDIR ${COAWST_DIR}


CMD ["/bin/bash"]