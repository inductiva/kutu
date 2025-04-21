FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/amr-wind-input-example.zip -P /home/ && \
    unzip /home/amr-wind-input-example.zip -d /home/ && \
    rm /home/amr-wind-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.0 as build

    # Fortran compiler
RUN export FC=/usr/bin/gfortran && \
    apt-get install -y libnetcdf-mpi-dev && \
    # Clone Openfast repository
    git clone --recursive --branch v3.4.0 https://github.com/Exawind/amr-wind.git amr-wind && \
    mkdir amr-wind/build && cd amr-wind/build && \
    cmake   -DAMR_WIND_ENABLE_OPENMP:BOOL=FALSE \
            -DCMAKE_BUILD_TYPE:STRING=RELEASE \
            -DAMR_WIND_ENABLE_NETCDF:BOOL=ON \
            -DAMR_WIND_ENABLE_MPI:BOOL=ON .. && \
    # Using -j may cause the build to fail
    make && \
    make install && \
    cd / && \
    rm -rf amr-wind

FROM ubuntu:22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean

COPY --from=build /usr/local/bin/ /usr/local/bin/

COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libmpi_cxx.so.40 /lib/x86_64-linux-gnu/libmpi_cxx.so.40
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1

COPY --from=test_env /home /home
