FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/swash-input-example.zip -P /home/ && \
    unzip /home/swash-input-example.zip -d /home/ && \
    rm /home/swash-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.0 as build

# Set SWASH options.
ARG SWASH_VERSION=9.01A
ARG SWASH_TMP=/tmp/swash

# Download, build, and install SWASH.
RUN mkdir ${SWASH_TMP}
WORKDIR ${SWASH_TMP}

RUN apt-get install ninja-build

RUN git clone https://gitlab.tudelft.nl/citg/wavemodels/swash.git && \
    cd swash && \
    git checkout 9abb83229bcb5d04543a5ddafe707d34a25f39c0 && \
    mkdir build && \
    cd build && \
    cmake .. -G Ninja -DMPI=ON -DCMAKE_Fortran_COMPILER=mpif90 -DCMAKE_INSTALL_PREFIX=/swash && \
    cmake --build . && \
    cmake --install . && \
    cd / && \
    rm -rf ${SWASH_TMP} && \
    sed -i '2i set -e' /swash/bin/swashrun && \
    sed -i 's/mpirun -np \$npmpi swash.exe/mpirun -np \$npmpi -machinefile machinefile swash.exe/' /swash/bin/swashrun



FROM ubuntu:22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean

ENV PATH /swash/bin:$PATH

COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /lib/x86_64-linux-gnu/libmpi_mpifh.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libgfortran.so.5 /lib/x86_64-linux-gnu/libgfortran.so.5
COPY --from=build /lib/x86_64-linux-gnu/libquadmath.so.0 /lib/x86_64-linux-gnu/libquadmath.so.0
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

COPY --from=build /swash /swash

COPY --from=test_env /home /home
