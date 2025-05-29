FROM inductiva/kutu:base-image_v0.1.1 as build

ENV DIR=/WRF/LIBRARIES
ENV CC=gcc
ENV CXX=g++
ENV FC=gfortran
ENV FCFLAGS="-m64 -fallow-argument-mismatch"
ENV F77=gfortran
ENV FFLAGS="-m64 -fallow-argument-mismatch"
ENV JASPERLIB=$DIR/grib2/lib
ENV JASPERINC=$DIR/grib2/include
ENV LDFLAGS=-L$DIR/grib2/lib
ENV CPPFLAGS=-I$DIR/grib2/include
ENV LIBS="-lnetcdf -lz"
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/WRF/LIBRARIES/grib2/lib/

ENV NETCDF=$DIR/netcdf
ENV LD_LIBRARY_PATH=$NETCDF/lib:$DIR/grib2/lib
ENV PATH=$NETCDF/bin:${PATH}
ENV JASPERLIB=$DIR/grib2/lib
ENV JASPERINC=$DIR/grib2/include
ENV WRF_DIR=/WRF/

RUN apt-get install csh perl -y && \
    git clone --recurse-submodules https://github.com/wrf-model/WRF.git && \
    cd WRF/ && \
    git checkout v4.6.1 && \
    mkdir LIBRARIES && \
    cd LIBRARIES/ && \
    wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/netcdf-c-4.7.2.tar.gz && \
    wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/netcdf-fortran-4.5.2.tar.gz && \
    wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/jasper-1.900.1.tar.gz && \
    wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/libpng-1.2.50.tar.gz && \
    wget https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compile_tutorial/tar_files/zlib-1.2.11.tar.gz && \
    tar -xvf netcdf-c-4.7.2.tar.gz && \
    tar -xvf netcdf-fortran-4.5.2.tar.gz && \
    tar -xvf jasper-1.900.1.tar.gz && \
    tar -xvf libpng-1.2.50.tar.gz && \
    tar -xvf zlib-1.2.11.tar.gz && \
    rm *.tar.gz && \
    export CC=gcc && \
    export CXX=g++ && \
    export FC=gfortran && \
    export FCFLAGS="-m64 -fallow-argument-mismatch" && \
    export F77=gfortran && \
    export FFLAGS="-m64 -fallow-argument-mismatch" && \
    export LDFLAGS="-L$NETCDF/lib -L$DIR/grib2/lib" && \
    export CPPFLAGS="-I$NETCDF/include -I$DIR/grib2/include -fcommon" && \
    cd zlib-1.2.11 && \
    ./configure --prefix=$DIR/grib2 && \
    make && \
    make install && \
    cd .. && \
    wget https://github.com/HDFGroup/hdf5/archive/hdf5-1_10_5.tar.gz && \
    tar xzvf hdf5-1_10_5.tar.gz && \
    cd hdf5-hdf5-1_10_5 && \
    ./configure --prefix=$DIR/netcdf --with-zlib=$DIR/grib2 --enable-fortran --enable-shared && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf hdf5* && \
    wget https://github.com/Unidata/netcdf-c/archive/v4.7.2.tar.gz && \
    tar xzvf v4.7.2.tar.gz && \
    cd netcdf-c-4.7.2 && \
    ./configure --prefix=$DIR/netcdf --disable-dap --enable-netcdf4 --enable-hdf5 --enable-shared && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf v4.7.2.tar.gz netcdf-c* && \
    export LIBS="-lnetcdf -lz" && \
    wget https://github.com/Unidata/netcdf-fortran/archive/v4.5.2.tar.gz && \
    tar xzvf v4.5.2.tar.gz && \
    cd netcdf-fortran-4.5.2 && \
    ./configure --prefix=$DIR/netcdf --disable-hdf5 --enable-shared && \
    make -j 4 && \
    make install && \
    cd .. && \
    rm -rf netcdf-fortran* v4.5.2.tar.gz && \
    cd libpng-1.2.50 && \
    ./configure --prefix=$DIR/grib2 && \
    make && \
    make install && \
    cd .. && \
    cd jasper-1.900.1 && \
    ./configure --prefix=$DIR/grib2 && \
    make && \
    make install && \
    cd /WRF/ && \
    cd share/ && \
    cp landread.c.dist landread.c && \
    cd /WRF/ && \
    printf "34\n1" | ./configure && \
    ./compile em_b_wave && \
    ./compile em_fire && \
    ./compile em_hill2d_x && \
    ./compile em_real && \
    ./compile em_squall2d_x && \
    ./compile em_convrad && \
    ./compile em_grav2d_x && \
    ./compile em_les && \
    ./compile em_scm_xy && \
    ./compile em_squall2d_y && \
    ./compile em_esmf_exp && \
    ./compile em_heldsuarez && \
    ./compile em_quarter_ss && \
    ./compile em_seabreeze2d_x && \
    ./compile em_tropical_cyclone && \
    git clone --recurse-submodules https://github.com/wrf-model/WPS.git && \
    cd WPS/ && \
    printf "3\n" |./configure && \
    ./compile

ENV PATH=/WRF/test/em_real/:/WRF/WPS/util/:$PATH

COPY ./functions/create_links.sh /scripts/create_links.sh
COPY ./functions/delete_links.sh /scripts/delete_links.sh

RUN chmod +x /scripts/create_links.sh && \
    chmod +x /scripts/delete_links.sh