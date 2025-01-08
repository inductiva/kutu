# Base image with Ubuntu 14.04
FROM ubuntu:14.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    subversion \
    gfortran \
    build-essential \
    mpich2 \
    perl \
    wget \
    make \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Install zlib
RUN wget https://www.zlib.net/fossils/zlib-1.2.8.tar.gz && \
    tar xvf zlib-1.2.8.tar.gz && \
    cd zlib-1.2.8 && \
    ./configure --prefix=/usr/local/zlib-1.2.8 && \
    make && \
    make install

# Install HDF5
RUN wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz && \
    tar xvf hdf5-1.8.13.tar.gz && \
    cd hdf5-1.8.13 && \
    ./configure --prefix=/usr/local/hdf5-1.8.13 --with-zlib=/usr/local/zlib-1.2.8 && \
    make && \
    make install

# Set environment variables for NetCDF installation
ENV CPPFLAGS="-I/usr/local/hdf5-1.8.13/include -I/usr/local/zlib-1.2.8/include" \
    LDFLAGS="-L/usr/local/hdf5-1.8.13/lib -L/usr/local/zlib-1.2.8/lib" \
    LD_LIBRARY_PATH="/usr/local/hdf5-1.8.13/lib:/usr/local/zlib-1.2.8/lib:/usr/local/netcdf.4.3.2/lib"

# Install NetCDF
RUN wget https://www.gfd-dennou.org/arch/ucar/netcdf/old/netcdf-4.3.2.tar.gz && \
    tar xvf netcdf-4.3.2.tar.gz && \
    cd netcdf-4.3.2 && \
    ./configure --prefix=/usr/local/netcdf.4.3.2 && \
    make && \
    make install

# Install NetCDF Fortran
RUN wget https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.4.0.tar.gz -O netcdf-fortran-4.4.0.tar.gz && \
    tar xvf netcdf-fortran-4.4.0.tar.gz && \
    cd netcdf-fortran-4.4.0 && \
    CPPFLAGS="-I/usr/local/netcdf.4.3.2/include" LDFLAGS="-L/usr/local/netcdf.4.3.2/lib" \
    ./configure --prefix=/usr/local/netcdf.4.3.2 && \
    make && \
    make install



# Set environment variables for COAWST
ENV MCT_INCDIR=/opt/COAWST/Lib/MCT/include \
    MCT_LIBDIR=/opt/COAWST/Lib/MCT/lib \
    NETCDF_INCDIR=/usr/local/netcdf.4.3.2/include \
    NETCDF_LIBDIR=/usr/local/netcdf.4.3.2/lib \
    NETCDF=/usr/local/netcdf.4.3.2

RUN apt-get update && apt-get install -y \
    git \
    ca-certificates 
# Clone COAWST from USGS GitHub and install MCT
RUN cd /opt && \
    git clone https://github.com/DOI-USGS/COAWST.git && \
    cd /opt/COAWST/Lib/MCT && \
    ./configure FC=mpif90 && \
    make && \
    make install

# Create COAWST directory
WORKDIR /opt/COAWST

# Make sure the build_coawst.sh script is executable
RUN chmod +x /opt/COAWST/build_coawst.sh

# Create a script to handle the COAWST build and ensure it runs correctly
RUN echo '#!/bin/bash\n\
cd /opt/COAWST\n\
# Make the build script executable (ensure permissions are correct)\n\
chmod +x build_coawst.sh\n\
# Run the build script\n\
./build_coawst.sh\n\
echo "Build process completed. Check for any errors above."\n\
/bin/bash' > /opt/COAWST/build_coawst_full.sh && chmod +x /opt/COAWST/build_coawst_full.sh

# Run the build script upon container start
CMD ["/opt/COAWST/build_coawst_full.sh"]
