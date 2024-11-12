FROM ubuntu:22.04 as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/erf-input-example.zip -P /home/ && \
    unzip /home/erf-input-example.zip -d /home/ && \
    rm /home/erf-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Ubuntu Image
FROM inductiva/kutu:base-image_v0.1.1 as build

ENV ERF_HOME=/ERF
ENV AMREX_HOME=/amrex

# Download openmpi and install
RUN git clone --recursive https://github.com/erf-model/ERF.git && \
    git clone https://github.com/amrex-codes/amrex.git && \
    cd ERF && \
    git checkout tags/24.11 && \
    mkdir mybuild && \
    cd /ERF/mybuild && \
    cmake -DCMAKE_BUILD_TYPE:STRING=Release \
      -DERF_ENABLE_MPI:BOOL=ON \
      -DAMReX_SPACEDIM:STRING=3 \
      -DERF_ENABLE_FCOMPARE:BOOL=ON \
      -DERF_ENABLE_TESTS:BOOL=ON \
      .. && \
    make && \
    make install

# Ubuntu Image
FROM ubuntu:22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean

COPY --from=test_env /home /home

COPY --from=build /usr/local/include/ /usr/local/include/

COPY --from=build /usr/local/share/amrex/ /usr/local/share/amrex/
COPY --from=build /usr/local/lib /usr/local/lib
COPY --from=build /usr/local/bin /usr/local/bin

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libmpi_cxx.so.40 /lib/x86_64-linux-gnu/libmpi_cxx.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
    