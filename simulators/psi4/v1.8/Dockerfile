# Use Ubuntu as base image
FROM inductiva/kutu:base-image_v0.1.1

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

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
    numpy \
    pytest \
    pytest-xdist \
    sphinx>=3.5 \
    nbsphinx \
    numpy \
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

# Clone PSI4 repository
RUN git clone https://github.com/psi4/psi4.git

# Build directory
WORKDIR /opt/psi4build/psi4



# Configure PSI4 with CMake
RUN cmake -S. -Bobjdir \
    -DCMAKE_INSTALL_PREFIX=/opt/psi4 \
    -DENABLE_MPI=ON \
    -DENABLE_GENERIC=ON \
    -DMAX_AM_ERI=3 \
    -DCMAKE_C_COMPILER=mpicc \
    -DCMAKE_CXX_COMPILER=mpicxx \
    -DCMAKE_Fortran_COMPILER=mpifort \
    -DBUILD_SHARED_LIBS=ON \
    && cd /opt/psi4build/psi4/objdir\
    && make -j$(nproc) \
    &&make install

RUN pip install numpy scipy msgpack-python networkx pint pydantic py-cpuinfo psutil

COPY ./test_sim.sh ./example.in /home/
RUN chmod +x /home/test_sim.sh /home/example.in
# Default command
WORKDIR /home
CMD ["psi4"]