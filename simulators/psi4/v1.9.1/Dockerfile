# Use Ubuntu as base image
FROM inductiva/kutu:base-image_v0.1.1

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ARG PSI4_VERSION=1.9.1
# Install basic build tools and pre-made Ubuntu dependencies
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    zlib1g-dev \
    libboost-all-dev \
    libeigen3-dev \
    libxml2-dev \
    perl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    numpy==1.21.0 \
    pytest \
    pytest-xdist \
    sphinx>=3.5 \
    nbsphinx \
    scipy \
    msgpack-python \
    networkx\
    pint \
    pydantic \
    py-cpuinfo \
    psutil \
    jupyter

# Set environment variables
ENV PATH="/opt/psi4/bin:${PATH}"


# Create working directory
WORKDIR /opt/psi4build

# Clone and build PSI4
RUN git clone --branch v${PSI4_VERSION} https://github.com/psi4/psi4.git \
    && cd psi4 \
    && cmake -S. -Bobjdir \
        -DCMAKE_INSTALL_PREFIX=/opt/psi4 \
        -DENABLE_MPI=ON \
        -DENABLE_GENERIC=ON \
        -DMAX_AM_ERI=3 \
        -DCMAKE_C_COMPILER=mpicc \
        -DCMAKE_CXX_COMPILER=mpicxx \
        -DCMAKE_Fortran_COMPILER=mpifort \
        -DBUILD_SHARED_LIBS=ON \
    && cd objdir \
    && make -j$(nproc) \
    && make install \
    && cd /opt/psi4build 


RUN pip install numpy scipy msgpack-python networkx pint pydantic py-cpuinfo psutil

COPY ./test_sim.sh ./example.in /home/
RUN chmod +x /home/test_sim.sh /home/example.in
# Default command
WORKDIR /home
CMD ["psi4"]