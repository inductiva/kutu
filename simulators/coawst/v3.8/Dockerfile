# Base image
FROM ubuntu:22.04

# Arguments for version control
ARG ZLIB_VERSION=1.2.8
ARG HDF5_VERSION=1.14.5
ARG NETCDF_C_VERSION=4.9.2
ARG NETCDF_FORTRAN_VERSION=4.5.4
ARG COAWST_COMMIT=f1a4250bc64bf0c4f9d521effb47d85837c92e8a

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    BASE_DIR=/opt \
    INSTALL_DIR=/usr/local \
    BUILD_DIR=/opt/COAWST

# Common compiler flags
ENV COMMON_FLAGS="-O2 -fPIC -fno-strict-aliasing -fno-lto -w" \
    CC=mpicc \
    CXX=mpicxx \
    FC=mpif90 \
    F77=mpif77

# Install base dependencies
RUN apt-get update && apt-get install -y \
    subversion gfortran build-essential m4 mpich perl wget make git \
    ca-certificates gcc curl libxml2-dev libcurl4-openssl-dev cmake \
    tcsh ksh csh binutils file zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${BASE_DIR}


# Install zlib
RUN wget https://www.zlib.net/fossils/zlib-${ZLIB_VERSION}.tar.gz && \
    tar xvf zlib-${ZLIB_VERSION}.tar.gz && \
    cd zlib-${ZLIB_VERSION} && \
    ./configure --prefix=${INSTALL_DIR}/zlib-${ZLIB_VERSION} && \
    make && make install && \
    cd .. && rm -rf zlib-${ZLIB_VERSION}*

# Install HDF5
ENV HDF5_DIR=${INSTALL_DIR}/hdf5-hdf5_${HDF5_VERSION}
RUN wget https://github.com/HDFGroup/hdf5/archive/refs/tags/hdf5_${HDF5_VERSION}.tar.gz && \
    tar xvf hdf5_${HDF5_VERSION}.tar.gz && \
    cd hdf5-hdf5_${HDF5_VERSION} && \
    ./configure --prefix=${HDF5_DIR} \
    --enable-parallel --enable-fortran --enable-shared \
    --with-zlib=${INSTALL_DIR}/zlib-${ZLIB_VERSION} \
    CC=${CC} FC=${FC} CXX=${CXX} && \
    make && make install && \
    cd .. && rm -rf hdf5-hdf5_${HDF5_VERSION}*

# Set environment variables for NetCDF
ENV NETCDF_DIR=${INSTALL_DIR}/netcdf \
    CPPFLAGS="-I${HDF5_DIR}/include -I${INSTALL_DIR}/zlib-${ZLIB_VERSION}/include" \
    LDFLAGS="-L${HDF5_DIR}/lib -L${INSTALL_DIR}/zlib-${ZLIB_VERSION}/lib" \
    LD_LIBRARY_PATH="${HDF5_DIR}/lib:${INSTALL_DIR}/zlib-${ZLIB_VERSION}/lib:${INSTALL_DIR}/netcdf/lib:${LD_LIBRARY_PATH}"

# Install NetCDF-C
RUN wget https://github.com/Unidata/netcdf-c/archive/refs/tags/v${NETCDF_C_VERSION}.tar.gz -O netcdf-c-4.9.2.tar.gz && \
    tar xvf netcdf-c-${NETCDF_C_VERSION}.tar.gz && \
    cd netcdf-c-${NETCDF_C_VERSION} && \
    ./configure --prefix=${NETCDF_DIR} \
    --enable-netcdf-4 --enable-shared --enable-parallel --enable-parallel-tests \
    CC=${CC} LIBS="-lhdf5_hl -lhdf5" && \
    make && make install && \
    cd .. && rm -rf netcdf-c-${NETCDF_C_VERSION}*

# Install NetCDF-Fortran
RUN wget https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v${NETCDF_FORTRAN_VERSION}.tar.gz -O netcdf-fortran-4.5.4.tar.gz && \
    tar xvf netcdf-fortran-${NETCDF_FORTRAN_VERSION}.tar.gz && \
    cd netcdf-fortran-${NETCDF_FORTRAN_VERSION} && \
    ./configure --prefix=${NETCDF_DIR} \
    FC=${FC} F77=${F77} CC=${CC} \
    CPPFLAGS="-I/usr/local/netcdf/include -I/usr/local/hdf5-hdf5_1.14.5/include" \
    LDFLAGS="-L/usr/local/netcdf/lib -L/usr/local/hdf5-hdf5_1.14.5/lib" \
    LIBS="-lnetcdf -lhdf5_hl -lhdf5" && \
    make && make install && \
    cd .. && rm -rf netcdf-fortran-${NETCDF_FORTRAN_VERSION}*


# COAWST environment setup
ENV MCT_INCDIR=/opt/COAWST/Lib/MCT/include \
    MCT_LIBDIR=/opt/COAWST/Lib/MCT/lib \
    MCT_DIR=${BASE_DIR}/COAWST/Lib/MCT \
    COAWST_DIR=/opt/COAWST \
    NETCDF_INCDIR=/usr/local/netcdf/include \
    NETCDF_LIBDIR=/usr/local/netcdf/lib \
    NETCDF=/usr/local/netcdf \
    NETCDF_CONFIG=/usr/local/netcdf/bin/nc-config \
    PATH="/usr/local/netcdf/bin:${PATH}" \
    FC=mpif90 \
    FCFLAGS="-O2 -fPIC -fno-strict-aliasing -fno-lto -w" \
    FFLAGS="-O2 -fPIC -fno-strict-aliasing -fno-lto -w" \
    LDFLAGS="-L/usr/local/netcdf/lib -L/usr/local/hdf5-hdf5_1.14.5/lib -L/usr/local/zlib-1.2.8/lib" \
    AR="gcc-ar" \
    RANLIB="gcc-ranlib" \
    NM="gcc-nm" \
    MY_ROOT_DIR=/opt/COAWST \
    MY_PROJECT_DIR=/opt/COAWST \
    MY_ROMS_SRC=/opt/COAWST \
    COAWST_APPLICATION=JOE_TC  \
    USE_MPI=ON \
    USE_MPIF90=ON \
    FORT=gfortran \
    WRF_DIR=/opt/COAWST/WRF \
    WW3_DIR=/opt/COAWST/WW3 \
    WWATCH3_DIR=/opt/COAWST/WW3 \
    WWATCH3_NETCDF=NC4 \
    MPICH_F90=gfortran \
    MPICH_FC=gfortran \
    MY_ANALYTICAL_DIR=${MY_PROJECT_DIR}/Projects/JOE_TC/Coupled \
    MY_HEADER_DIR=${MY_PROJECT_DIR}/Projects/JOE_TC/Coupled \
    SWAN_DIR=/opt/COAWST/SWAN \
    WRF_EM_CORE=1 \
    NETCDF4=1 \
    NETCDF_classic=1 \
    WRFIO_NCD_LARGE_FILE_SUPPORT=1 \
    HDF5=/usr/local/hdf5-hdf5_1.14.5 \
    PHDF5=/usr/local/hdf5-hdf5_1.14.5 \
    PATH=/usr/local/netcdf/bin:$PATH \
    LD_LIBRARY_PATH=/usr/local/netcdf/lib:/usr/local/hdf5-hdf5_1.14.5/lib:$LD_LIBRARY_PATH \
    MY_CPP_FLAGS="-DDUCKNC -DWEC_VF -DROLLER_RENIERS -DAVERAGES_WEC"




# Clone and setup COAWST
RUN cd ${BASE_DIR} && \
    git clone https://github.com/DOI-USGS/COAWST.git && \
    cd COAWST && \
    git checkout ${COAWST_COMMIT}

# Build MCT
RUN cd ${MCT_DIR} && \
    ./configure FC=${FC} FCFLAGS="${COMMON_FLAGS}" \
    LDFLAGS="-fno-strict-aliasing -fno-lto -w" \
    AR="ar cr" ARFLAGS="" RANLIB="ranlib" \
    --prefix=${MCT_DIR} && \
    sed -i 's/ar libmpeu.a/ar cr libmpeu.a/g' mpeu/Makefile && \
    make && make install

# Build SCRIP_COAWST
RUN cd ${COAWST_DIR}/Lib/SCRIP_COAWST && \
    sed -i -e 's/FORT = .*/FORT = gfortran/' \
           -e 's/FC = .*/FC = mpif90/' \
           -e "s/FCFLAGS = .*/FCFLAGS = ${COMMON_FLAGS}/" \
           -e 's/LDFLAGS = .*/LDFLAGS = -fno-strict-aliasing -fno-lto -w/' \
           -e 's/USE_MPI=.*/USE_MPI=on/' \
           -e 's/USE_MPIF90=.*/USE_MPIF90=on/' \
           makefile && \
    make -j1

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
    ./build_coawst_ducknc.sh

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
    ./build_coawst_estuary.sh 
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
    ./build_coawst_inlet.sh

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
    ./build_coawst_inlet_diffgrid.sh

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test_diffgrid

# Configure COAWST build environment for INLET_TEST InWave
RUN cd ${COAWST_DIR} && \
    cp build_coawst.sh build_coawst_inlet_inwave.sh && \
    chmod +x build_coawst_inlet_inwave.sh && \
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
    ./build_coawst_inlet_inwave.sh

# Rename the executable
RUN mv ${COAWST_DIR}/coawstM ${COAWST_DIR}/coawstM_Inlet_test_inwave

# Copy test simulation script
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

WORKDIR ${COAWST_DIR}


CMD ["/bin/bash"]