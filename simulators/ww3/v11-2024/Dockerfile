FROM ubuntu:22.04 as build

ENV WWATCH3_NETCDF=NC4
ENV NETCDF_CONFIG=/WW3_LIBRARIES/bin/nf-config
ENV WW3=/WW3

ENV FCFLAGS="-fallow-argument-mismatch"
ENV FFLAGS="-fallow-argument-mismatch"

ENV DIR=/WW3_LIBRARIES

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget tar gcc gfortran m4 git cmake && \
    apt-get install build-essential -y && \
    mkdir /LIBRARIES && \
    mkdir /WW3_LIBRARIES && \
    cd /LIBRARIES/ && \
    wget https://curl.se/download/curl-7.64.0.tar.gz && \
    tar -xf curl-7.64.0.tar.gz && \
    cd curl-7.64.0 && \
    ./configure --prefix=$DIR && \
    make -j && \
    make install && \
    cd .. && \
    wget https://zlib.net/fossils/zlib-1.2.11.tar.gz && \
    tar -xf zlib-1.2.11.tar.gz && \
    cd zlib-1.2.11 && \
    ./configure --prefix=$DIR && \
    make -j && \
    make install && \
    cd .. && \
    wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.5/src/hdf5-1.10.5.tar && \
    tar -xf hdf5-1.10.5.tar && \
    cd hdf5-1.10.5 && \
    ./configure --prefix=$DIR --with-zlib=$DIR && \
    make -j && \
    make install && \
    cd .. && \
    wget https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.6.1.tar.gz && \
    tar -xf v4.6.1.tar.gz && \
    cd netcdf-c-4.6.1 && \
    CPPFLAGS=-I$DIR/include LDFLAGS=-L$DIR/lib ./configure --prefix=$DIR && \
    make -j && \
    make install && \
    cd .. && \
    wget https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.4.4.tar.gz && \
    tar -xf v4.4.4.tar.gz && \
    cd netcdf-fortran-4.4.4 && \
    CPPFLAGS=-I$DIR/include LDFLAGS=-L$DIR/lib ./configure --prefix=$DIR && \
    make -j && \
    make install

ENV LD_LIBRARY_PATH=$DIR/lib:$LD_LIBRARY_PATH
ENV PATH=$DIR/bin:$PATH

RUN apt-get install -y libopenmpi-dev=4.1.2-2ubuntu1 \
    openmpi-bin=4.1.2-2ubuntu1 && \
    apt-get update && \
    apt install ssh rsync -y && \
    git clone https://github.com/NOAA-EMC/WW3.git && \
    cd WW3/ && \
    git checkout 7705171721e825d58e1e867e552e328fc812bfdd && \
    echo -e ".\nn\nn" | sh model/bin/ww3_from_ftp.sh

# Install METIS 5.1.0
RUN wget https://karypis.github.io/glaros/files/sw/metis/metis-5.1.0.tar.gz && \
    tar -xzf metis-5.1.0.tar.gz && \
    cd metis-5.1.0 && \
    make config shared=1 prefix=/usr/local && \
    make && make install && \
    cd .. && rm -rf metis-5.1.0 metis-5.1.0.tar.gz

# Install ParMETIS 4.0.3
RUN wget https://karypis.github.io/glaros/files/sw/parmetis/parmetis-4.0.3.tar.gz && \
    tar -xzf parmetis-4.0.3.tar.gz && \
    cd parmetis-4.0.3 && \
    make config shared=1 prefix=/usr/local && \
    make && make install && \
    cd .. && rm -rf parmetis-4.0.3 parmetis-4.0.3.tar.gz

ENV METIS_PATH=/usr/local \
    LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH \
    LIBRARY_PATH=/usr/local/lib:$LIBRARY_PATH \
    CPATH=/usr/local/include:$CPATH 

RUN cd /WW3 && \
    mkdir build && \
    cd build/ && \
    cmake .. -DSWITCH=Ifremer2 -DNetCDF_INCLUDE_DIRS=/WW3_LIBRARIES/include \
      -DNetCDF_LIBRARIES="/WW3_LIBRARIES/lib/libnetcdf.so;/WW3_LIBRARIES/lib/libnetcdff.so" \
      -DNetCDF_C_LIBRARY=/WW3_LIBRARIES/lib/libnetcdf.so \
      -DNetCDF_F90_LIBRARY=/WW3_LIBRARIES/lib/libnetcdff.so && \
    make -j && \
    make install

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

COPY ./compile_ww3.sh /home/compile_ww3.sh
RUN chmod +x /home/compile_ww3.sh
