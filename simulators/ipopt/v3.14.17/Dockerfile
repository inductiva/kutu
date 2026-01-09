FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    g++ \
    gfortran \
    make \
    wget \
    git \
    pkg-config \
    libblas-dev \
    liblapack-dev \
    libmetis-dev \
    libopenblas-dev \
    libtool \
    coinor-libcoinutils-dev \
    coinor-libosi-dev \
    coinor-libcoinmp-dev \
    libomp-dev \
    cmake \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt

# Download and build IPOPT
RUN git clone https://github.com/coin-or/Ipopt.git && \
    cd Ipopt && \
    git checkout stable/3.14

RUN git clone https://github.com/coin-or-tools/ThirdParty-ASL.git && \
    cd ThirdParty-ASL && \
    ./get.ASL && \
    ./configure && \
    make && \
    make install

# Download and build thirdparty MUMPS with OpenMP
RUN git clone https://github.com/coin-or-tools/ThirdParty-Mumps.git && \
    cd ThirdParty-Mumps && \
    ./get.Mumps && \
    ./configure && \
    make && \
    make install

# Enable OpenMP for MUMPS
ENV CXXFLAGS="-fopenmp"
ENV FFLAGS="-fopenmp"
ENV CFLAGS="-fopenmp"

# Configure and build IPOPT
RUN cd Ipopt && \
    mkdir build && cd build && \
    ../configure --prefix=/opt/ipopt-install && \
    make -j$(nproc) && make install

# Environment variables for IPOPT
ENV LD_LIBRARY_PATH="/usr/local/lib/:${LD_LIBRARY_PATH}"
ENV PATH="/opt/ipopt-install/bin:${PATH}"
ENV PKG_CONFIG_PATH="/opt/ipopt-install/lib/pkgconfig:${PKG_CONFIG_PATH}"

# Test IPOPT install
RUN echo 'int main() { return 0; }' > test.cpp && \
    g++ test.cpp -o test $(pkg-config --cflags --libs ipopt) && \
    ./test

# HiGHS

RUN cd / && \
    git clone https://github.com/ERGO-Code/HiGHS.git && \
    cd HiGHS && \
    cmake -S. -B build && \
    cmake --build build --parallel

# GLPK
RUN wget http://ftp.gnu.org/gnu/glpk/glpk-5.0.tar.gz && \
    gzip -d glpk-5.0.tar.gz && \
    tar -x < glpk-5.0.tar && \
    cd glpk-5.0 && \
    ./configure && \
    make && \
    make install



COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh