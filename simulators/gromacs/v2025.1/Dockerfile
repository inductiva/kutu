FROM ubuntu:22.04 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/gromacs-input-example.zip -P /home/ && \
    unzip /home/gromacs-input-example.zip -d /home/ && \
    rm /home/gromacs-input-example.zip
    
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 as build

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

RUN apt-get update \
    && apt-get install -y \
    fftw3-dev pkg-config \
    build-essential \
    openmpi-common \
    libopenmpi-dev \
    openssh-client \
    openmpi-bin \
    liblapack3 \
    libgomp1 \
    python3 \
    fftw3 \
    unzip \
    wget \
    libssl-dev && \
    # Install cmake
    wget -O cmake.tar.gz https://github.com/Kitware/CMake/archive/refs/tags/v3.31.5.tar.gz && \
    tar -xzf cmake.tar.gz && ls && cd CMake-3.31.5 && \
    ./bootstrap && make -j$(nproc) && make install && \
    cd / && \
    wget https://github.com/gromacs/gromacs/archive/refs/tags/v2025.1.zip -P / && \
    unzip /v2025.1.zip -d / && \
    rm /v2025.1.zip && \
    cd gromacs-2025.1 && \
    mkdir build && \
    cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON -DGMX_GPU=OFF -DGMX_MPI=on && \
    make && \
    #check can fail if the computer is slow or has few resources
    #make check && \
    make install && \
    . /usr/local/gromacs/bin/GMXRC && \
    mv /usr/local/gromacs/bin/gmx_mpi /usr/local/gromacs/bin/gmx && \
    rm -r /gromacs-2025.1

FROM ubuntu:22.04 

COPY --from=build /usr/local/gromacs /usr/local/gromacs

ENV PATH="${PATH}:/usr/local/gromacs/bin/"
    
COPY --from=test_env /home /home

RUN apt-get update -y && \
    apt-get install -y openmpi-bin

COPY --from=build /usr/lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /usr/lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /usr/lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /usr/lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /usr/lib/x86_64-linux-gnu/libopen-rte.so.40 /usr/lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /usr/lib/x86_64-linux-gnu/libopen-pal.so.40 /usr/lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /usr/lib/x86_64-linux-gnu/libhwloc.so.15 /usr/lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libmpi.so.40 /usr/lib/x86_64-linux-gnu/libmpi.so.40
