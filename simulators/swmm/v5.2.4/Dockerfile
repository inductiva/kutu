FROM ubuntu:22.04 AS build

ARG DEBIAN_FRONTEND=noninteractive
ARG SWMM_VERSION=5.2.4
ARG SWMM_SRC_URL=https://www.epa.gov/system/files/other-files/2023-08/swmm524_engine.zip

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        cmake \
        wget \
        unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/swmm

RUN wget -O swmm.zip ${SWMM_SRC_URL} && \
    unzip -q swmm.zip && \
    mv swmm524_engine swmm-${SWMM_VERSION} && \
    rm swmm.zip

WORKDIR /tmp/swmm/swmm-${SWMM_VERSION}

RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build -j"$(nproc)" && \
    install -d /opt/swmm/bin /opt/swmm/lib && \
    cp build/runswmm /opt/swmm/bin/ && \
    cp build/libswmm5.so /opt/swmm/lib/

FROM ubuntu:22.04 AS openmpi-build

ARG DEBIAN_FRONTEND=noninteractive
ARG OPENMPI_VERSION=4.1.6
ARG OPENMPI_SRC_URL=https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-${OPENMPI_VERSION}.tar.gz

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        wget \
        ca-certificates \
        libevent-dev \
        libhwloc-dev \
        libudev-dev \
        libnuma-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/openmpi

RUN wget -O openmpi.tar.gz ${OPENMPI_SRC_URL} && \
    tar -xzf openmpi.tar.gz && \
    rm -f openmpi.tar.gz

WORKDIR /tmp/openmpi/openmpi-${OPENMPI_VERSION}

RUN ./configure --prefix=/opt/openmpi/${OPENMPI_VERSION} && \
    make -j"$(nproc)" && \
    make install

FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG OPENMPI_VERSION=4.1.6

RUN apt-get update && \
    apt-get install -y \
        libgomp1 \
        ca-certificates \
        libevent-2.1-7 \
        libhwloc15 \
        libudev1 \
        libnuma1 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/swmm /opt/swmm
COPY --from=openmpi-build /opt/openmpi /opt/openmpi

RUN printf '/opt/swmm/lib\n/opt/openmpi/%s/lib\n' "$OPENMPI_VERSION" > /etc/ld.so.conf.d/swmm_openmpi.conf && \
    ldconfig

ENV PATH="/opt/swmm/bin:/opt/openmpi/${OPENMPI_VERSION}/bin:${PATH}" \
    MPIRUN_BIN_PATH_TEMPLATE="/opt/openmpi/${OPENMPI_VERSION}/bin/mpirun"

RUN ln -s /opt/swmm/bin/runswmm /usr/local/bin/runswmm

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh
