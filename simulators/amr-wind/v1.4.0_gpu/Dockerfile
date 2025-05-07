FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/amr-wind-input-example.zip -P /home/ && \
    unzip /home/amr-wind-input-example.zip -d /home/ && \
    rm /home/amr-wind-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 AS build

    # Fortran compiler
RUN export FC=/usr/bin/gfortran && \
    apt-get update && \
    apt-get  install -y libnetcdf-mpi-dev \
    git cmake gfortran \
    libopenmpi-dev=4.1.2-2ubuntu1 \
    openmpi-common=4.1.2-2ubuntu1 \
    openmpi-bin=4.1.2-2ubuntu1 \
    libnetcdff-dev \
    libnetcdf-dev && \
    cp /usr/lib/x86_64-linux-gnu/netcdf/mpi/include/netcdf_par.h /usr/include/ && \
    # Clone Openfast repository
    git clone --recursive --branch v1.4.0 https://github.com/Exawind/amr-wind.git amr-wind && \
    mkdir amr-wind/build && cd amr-wind/build && \
    cmake   -DAMR_WIND_ENABLE_OPENMP:BOOL=FALSE \
            -DCMAKE_BUILD_TYPE:STRING=RELEASE \
            -DAMR_WIND_ENABLE_NETCDF:BOOL=ON \
            -DAMR_WIND_ENABLE_CUDA:BOOL=ON \
            -DAMR_WIND_ENABLE_MPI:BOOL=ON .. && \
    # Using -j may cause the build to fail
    make && \
    make install && \
    cd / && \
    rm -rf amr-wind

FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean

COPY --from=build /usr/local/bin/ /usr/local/bin/

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/ /lib/x86_64-linux-gnu/

COPY --from=test_env /home /home