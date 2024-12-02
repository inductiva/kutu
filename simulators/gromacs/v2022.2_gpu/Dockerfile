
FROM ubuntu:22.04 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/gromacs-input-example.zip -P /home/ && \
    unzip /home/gromacs-input-example.zip -d /home/ && \
    rm /home/gromacs-input-example.zip
    
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 as build

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
    cmake \
    unzip \
    wget && \
    wget https://github.com/gromacs/gromacs/archive/refs/tags/v2022.2.zip -P / && \
    unzip /v2022.2.zip -d / && \
    rm /v2022.2.zip && \
    cd gromacs-2022.2 && \
    mkdir build && \
    cd build && \
    cmake .. -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON -DGMX_GPU=CUDA -DGMX_MPI=on && \
    make && \
    #check can fail if the computer is slow or has few resources
    #make check && \
    make install && \
    . /usr/local/gromacs/bin/GMXRC && \
    mv /usr/local/gromacs/bin/gmx_mpi /usr/local/gromacs/bin/gmx && \
    rm -r /gromacs-2022.2

FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04 

COPY --from=build /usr/local/gromacs /usr/local/gromacs

ENV PATH="${PATH}:/usr/local/gromacs/bin/"
    
COPY --from=test_env /home /home

RUN apt-get update -y && \
    apt-get install -y openmpi-bin

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libgomp.so.1 /lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /usr/local/cuda/lib64/libcufft.so.11 /usr/local/cuda/lib64/libcufft.so.11
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /usr/local/gromacs/bin//../lib/libgromacs_mpi.so.7 /usr/local/gromacs/bin//../lib/libgromacs_mpi.so.7
COPY --from=build /usr/local/gromacs/bin//../lib/../lib/libmuparser.so.2 /usr/local/gromacs/bin//../lib/../lib/libmuparser.so.2
