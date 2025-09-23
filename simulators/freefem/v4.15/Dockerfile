FROM inductiva/kutu:base-image_v0.1.1 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/freefem-input-example.zip -P /home/ && \
    unzip /home/freefem-input-example.zip -d /home/ && \
    rm /home/freefem-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 as build

RUN apt-get update && \
    apt-get install -y \
    openmpi-common=4.1.2-2ubuntu1 \
    openmpi-bin=4.1.2-2ubuntu1 \
    libopenmpi-dev=4.1.2-2ubuntu1 \
    cpp freeglut3-dev g++ gcc gfortran \
    m4 make patch pkg-config wget python3 unzip \
    liblapack-dev libhdf5-dev libgsl-dev software-properties-common \
    autoconf automake autotools-dev bison flex gdb git cmake && \
    git clone --branch v4.15 https://github.com/FreeFem/FreeFem-sources.git && \
    cd /FreeFem-sources && \
    autoreconf -i && \
    ./configure --enable-download --enable-generic --enable-optim --with-mpi=openmpi --prefix=/opt/FreeFem && \
    #One of the downloads fails
    ./3rdparty/getall -a || true && \
    cd 3rdparty/ff-petsc && \
    #add flag to makefile to download cmake
    sed -i 's|^\(\./configure\) --prefix=\$(DIR_INSTALL_REAL)|\1 --download-cmake --prefix=$(DIR_INSTALL_REAL)|' Makefile && \
    make petsc-slepc && \
    cd /FreeFem-sources && \
    ./reconfigure && \
    make -j && \
    #Done manually
    #make check && \
    make install && \
    rm -r /FreeFem-sources

ENV PATH="/opt/FreeFem/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/FreeFem/lib:${LD_LIBRARY_PATH}"

COPY --from=test_env /home /home