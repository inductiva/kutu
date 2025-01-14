# Base image with Ubuntu 22.04
FROM ubuntu:22.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    subversion \
    gfortran \
    build-essential \
    m4 \
    mpich \
    perl \
    wget \
    make \
    git \
    ca-certificates \
    gcc \
    curl \
    libxml2-dev \
    libcurl4-openssl-dev \ 
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Install zlib
RUN wget https://www.zlib.net/fossils/zlib-1.2.8.tar.gz && \
    tar xvf zlib-1.2.8.tar.gz && \
    cd zlib-1.2.8 && \
    ./configure --prefix=/usr/local/zlib-1.2.8 && \
    make && \
    make install && \
    cd .. && rm -rf zlib-1.2.8* 

# Install HDF5 1.14.5
RUN wget https://github.com/HDFGroup/hdf5/archive/refs/tags/hdf5_1.14.5.tar.gz && \
    tar xvf hdf5_1.14.5.tar.gz && \
    cd hdf5-hdf5_1.14.5 && \  
    ./configure --prefix=/usr/local/hdf5-hdf5_1.14.5 --with-zlib=/usr/local/zlib-1.2.8 && \
    make && \
    make install && \
    cd .. && rm -rf hdf5-hdf5_1.14.5* 

# Set environment variables for NetCDF installation
ENV CPPFLAGS="-I/usr/local/hdf5-hdf5_1.14.5/include -I/usr/local/zlib-1.2.8/include" \
    LDFLAGS="-L/usr/local/hdf5-hdf5_1.14.5/lib -L/usr/local/zlib-1.2.8/lib" \
    LD_LIBRARY_PATH="/usr/local/hdf5-hdf5_1.14.5/lib:/usr/local/zlib-1.2.8/lib:/usr/local/netcdf/lib"


# Install NetCDF
RUN wget https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.9.2.tar.gz -O netcdf-c-4.9.2.tar.gz && \
    tar xvf netcdf-c-4.9.2.tar.gz && \
    cd netcdf-c-4.9.2 && \
    ./configure --prefix=/usr/local/netcdf && \
    make && \
    make install && \
    cd .. && rm -rf netcdf-c-4.9.2*


# Install NetCDF Fortran
RUN wget https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.5.4.tar.gz -O netcdf-fortran-4.5.4.tar.gz && \
    tar xvf netcdf-fortran-4.5.4.tar.gz && \
    cd netcdf-fortran-4.5.4 && \
    CPPFLAGS="-I/usr/local/netcdf/include" LDFLAGS="-L/usr/local/netcdf/lib" \
    ./configure --prefix=/usr/local/netcdf && \
    make && \
    make install && \
    cd .. && rm -rf netcdf-fortran-4.5.4*




# Set environment variables for COAWST
ENV MCT_INCDIR=/opt/COAWST/Lib/MCT/include \
    MCT_LIBDIR=/opt/COAWST/Lib/MCT/lib \
    NETCDF_INCDIR=/usr/local/netcdf/include \
    NETCDF_LIBDIR=/usr/local/netcdf/lib \
    NETCDF=/usr/local/netcdf \
    NETCDF_CONFIG=/usr/local/netcdf/bin/nc-config \
    PATH="/usr/local/netcdf/bin:${PATH}" \
    FC=mpif90 \
    FCFLAGS="-O2 -fPIC" \
    LDFLAGS="-L/usr/local/netcdf/lib -L/usr/local/hdf5-hdf5_1.14.5/lib -L/usr/local/zlib-1.2.8/lib"



# Clone COAWST and build MCT 
RUN cd /opt && \
    git clone https://github.com/DOI-USGS/COAWST.git && \
    cd COAWST && \
    git checkout f1a4250bc64bf0c4f9d521effb47d85837c92e8a && \
    cd Lib/MCT && \
    ./configure FC=mpif90 FCFLAGS="-O2 -fPIC" && \
    make && \
    make install && \
    rm -rf /opt/COAWST/.git

# Install SCRIP_COAWST
RUN cd /opt/COAWST/Lib/SCRIP_COAWST && \
    sed -i 's/FORT = .*/FORT = gfortran/' makefile && \
    sed -i 's/FC = .*/FC = mpif90/' makefile && \
    sed -i 's/FCFLAGS = .*/FCFLAGS = -O2 -fPIC/' makefile && \
    sed -i 's/USE_MPI=.*/USE_MPI=on/' makefile && \
    sed -i 's/USE_MPIF90=.*/USE_MPIF90=on/' makefile && \
    make -j1

    # Copy test simulation script
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Create COAWST directory
WORKDIR /opt/COAWST/Lib/SCRIP_COAWST



# Cleanup unnecessary files
RUN rm -rf /opt/*.tar.gz

# Run the build script upon container start
CMD ["/home/test_sim.sh"]
