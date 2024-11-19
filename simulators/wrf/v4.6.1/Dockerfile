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
ENV PATH=$DIR/netcdf/bin:$PATH
ENV NETCDF=$DIR/netcdf
ENV LIBS="-lnetcdf -lz"


RUN apt-get install csh perl && \
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
    cd netcdf-c-4.7.2 && \
    ./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared && \
    make && \
    make install && \
    cd .. && \
    cd netcdf-fortran-4.5.2 && \
    ./configure --prefix=$DIR/netcdf --disable-dap --disable-netcdf-4 --disable-shared && \
    make && \
    make install && \
    cd .. && \
    cd zlib-1.2.11 && \
    ./configure --prefix=$DIR/grib2 && \
    make && \
    make install && \
    cd .. && \
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
    #here we need  32. (serial)  33. (smpar)  34. (dmpar)  35. (dm+sm)   GNU (gfortran/gcc)
    # 34
    echo -e "34\n1\n" | ./configure 

    #we can now compile by doing ./compile <case_name>


