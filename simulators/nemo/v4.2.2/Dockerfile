FROM inductiva/kutu:base-image_v0.1.1 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/amr-wind-input-example.zip -P /home/ && \
    unzip /home/amr-wind-input-example.zip -d /home/ && \
    rm /home/amr-wind-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 as build

#Source https://github.com/rcaneill/xnemogcm_test_data/blob/master/src/4.2.0/apptainer-nemo.def
ENV WORKDIR=/nemo/sources
ENV INSTDIR=/nemo/installs

# compilers
ENV CC=/usr/bin/mpicc
ENV CXX=/usr/bin/mpicxx
ENV FC=/usr/bin/mpif90
ENV F77=/usr/bin/mpif77
# compiler flags (except for libraries)
ENV CFLAGS="-O3 -fPIC"
ENV CXXFLAGS="-O3 -fPIC"
ENV F90FLAGS="-O3 -fPIC"
ENV FCFLAGS="-O3 -fPIC"
ENV FFLAGS="-O3 -fPIC"
ENV LDFLAGS="-O3 -fPIC "
# FLAGS FOR F90  TEST-EXAMPLES
ENV FCFLAGS_f90="-O3 -fPIC "

RUN apt -y update && \
    apt -y install  openmpi-bin \
                    libmpich-dev \
                    libopenmpi-dev \
                    gcc \
                    g++ \
                    gfortran \
                    subversion \
                    libcurl4-openssl-dev \
                    wget \
                    make \
                    m4 \
                    git \
                    liburi-perl \
                    libxml2-dev

RUN mkdir -p $WORKDIR && \
    mkdir -p $INSTDIR && \
    cd $WORKDIR && \
    mkdir -p ZLIB && \
    cd ZLIB && \
    LIB_VERSION="zlib-1.3.1" && \
    LIB_FILE="${LIB_VERSION}.tar.gz" && \
    wget https://www.zlib.net/${LIB_FILE} && \
    tar xvfz $LIB_FILE && \
    cd $LIB_VERSION && \
    ./configure --prefix=$INSTDIR && \
    make -j 4 && \
    make install
    
    # install hdf5
RUN cd $WORKDIR && \
    mkdir -p HDF5 && \
    cd HDF5 && \
    LIB_VERSION="hdf5-1.10.5" && \
    LIB_FILE="${LIB_VERSION}.tar.gz" && \
    wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.5/src/hdf5-1.10.5.tar.gz && \
    tar xvfz $LIB_FILE && \
    cd $LIB_VERSION && \
    export HDF5_Make_Ignore=yes && \
    # Configure
    ./configure --prefix=$INSTDIR \
       	    --enable-fortran  --enable-parallel --enable-hl --enable-shared  \
            --with-zlib=$INSTDIR && \
    # Make and install
    make -j 4 && \
    make install

    # install netcdf-c
RUN cd $WORKDIR && \
    mkdir -p NetCDF-c && \
    cd NetCDF-c && \
    LIB_VERSION="4.9.2" && \
    LIB_FILE="v${LIB_VERSION}.tar.gz" && \
    wget https://github.com/Unidata/netcdf-c/archive/${LIB_FILE} && \
    tar xvfz $LIB_FILE && \
    cd netcdf-c-${LIB_VERSION} && \
    export CPPFLAGS="-I$INSTDIR/include -DpgiFortran" && \
    export LDFLAGS="-Wl,-rpath,$INSTDIR/lib -L$INSTDIR/lib -lhdf5_hl -lhdf5" && \
    export LIBS="-lmpi" && \
    ./configure --prefix=$INSTDIR --enable-netcdf-4 --enable-shared \
                --enable-parallel-tests && \
    make -j 4 && \
    make install

    # Install netcdf-fortran
RUN cd $WORKDIR && \
    mkdir -p NetCDF-fortran && \
    cd NetCDF-fortran && \
    LIB_VERSION="4.6.0" && \
    LIB_FILE="v${LIB_VERSION}.tar.gz" && \
    wget https://github.com/Unidata/netcdf-fortran/archive/${LIB_FILE} && \
    tar xvfz $LIB_FILE && \
    cd netcdf-fortran-${LIB_VERSION} && \
    export LD_LIBRARY_PATH=${NCDIR}/lib:${LD_LIBRARY_PATH} && \
    export CPPFLAGS="-I$INSTDIR/include -DpgiFortran" && \
    export LDFLAGS="-Wl,-rpath,$INSTDIR/lib -L$INSTDIR/lib -lnetcdf -lhdf5_hl -lhdf5 -lz -lcurl" && \
    export LIBS="-lmpi" && \
    ./configure --prefix=$INSTDIR \
                --enable-shared --enable-parallel-tests \
                --enable-parallel && \
    make -j 4 && \
    make install

    # Install xios
RUN cd $WORKDIR && \
    mkdir -p XIOS && \
    cd XIOS && \
    svn --trust-server-cert-failures="other,unknown-ca,cn-mismatch,expired"  --non-interactive  co -r 2481 http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/trunk xios-trunk

COPY ./arch_xios/arch-GCC_LINUX_local.env $WORKDIR/XIOS/xios-trunk/arch/arch-GCC_LINUX.env
COPY ./arch_xios/arch-GCC_LINUX_local.path $WORKDIR/XIOS/xios-trunk/arch/arch-GCC_LINUX.path
COPY ./arch_xios/arch-GCC_LINUX_local.fcm $WORKDIR/XIOS/xios-trunk/arch/arch-GCC_LINUX.fcm

RUN cd $WORKDIR/XIOS/xios-trunk && \
    ./make_xios --arch GCC_LINUX --job 4 && \
    cd .. && \
    ln -s xios-trunk xios

    # Install nemo
RUN cd $WORKDIR && \
    mkdir -p NEMO && \
    cd NEMO && \
    git clone --branch 4.2.0 https://forge.nemo-ocean.eu/nemo/nemo.git NEMOGCM

COPY ./arch_nemo/arch-local.fcm $WORKDIR/NEMO/NEMOGCM/arch/arch-local.fcm

RUN cd $WORKDIR/NEMO/NEMOGCM/cfgs && \
    cp -r GYRE_PISCES/ GYRE && \
    echo "GYRE                 OCE" >> ref_cfgs.txt && \
    cd GYRE && \
    rm *.fcm && \
    echo "bld::tool::fppkeys   key_xios key_qco" >> cpp_GYRE.fcm && \
    cd EXPREF && \
    rm namelist_top* namelist_pisces* field_def_nemo-pisces.xml && \
    cd ../../.. && \
    # Compile
    ./makenemo -m local -r GYRE -n GYRE_xnemogcm -j 4

    
#     ./makenemo -[aru] CONFIG -m ARCH [-[dehjntv] ...] [{list_key,clean,clean_config}]
#                                                   [{add_key,del_key} ...]

# Mandatory
#    -m    Computing architecture (./arch), FCM file describing the compilation settings

#    and one of the following option (use 'all' arg to list available items)

#    -r    Reference configuration (./cfgs), proven with long-term support
#    -a    Academic test case (./tests), ready-to-use configuration with no support over time
#    -u    Scripted remote configuration (see ./tests/rmt_cfgs.txt)

# Optional
#    -d    New set of sub-components (subfolders from ./src directory)
#    -e    Path for alter patch  location (default: 'MY_SRC' in configuration folder)
#    -h    Print this help
#    -j    Number of processes to compile (0: dry run with no build)
#    -n    Name for new configuration
#    -s    Path for alter source location (default: 'src' root directory)
#    -t    Path for alter build  location (default: 'BLD' in configuration folder)
#    -v    Level of verbosity ([0-3])

# Examples
#    ¤ Configuration creation
#         Build          : ./makenemo         -[aru] ... [...]
#         Copy           : ./makenemo -n ...  -[aru] ... [...]
#    ¤ Configuration management
#         List CPP keys  : ./makenemo -n ... list_key
#         Add-Remove keys: ./makenemo -n ... add_key '...' del_key '...'
#         Fresh start    : ./makenemo -n ... clean
#         Removal        : ./makenemo -n ... clean_config



# bsdmainutils -y && \
#     wget https://forge.nemo-ocean.eu/nemo/nemo/-/archive/4.2.2/nemo-4.2.2.zip && \
#     unzip nemo-4.2.2.zip && \
#     rm nemo-4.2.2.zip && \
#     cd nemo-4.2.2 && \
#     cd arch && \
#     sed -i 's|/lib/|/lib/x86_64-linux-gnu/|g' build_arch-auto.sh
#     ./build_arch-auto.sh 