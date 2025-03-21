FROM ubuntu:22.04 AS test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/reef3d-input-example.zip -P /home/ && \
    unzip /home/reef3d-input-example.zip -d /home/ && \
    rm /home/reef3d-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# ubuntu base image
FROM inductiva/kutu:base-image_v0.1.1

ARG REEF3D_VERSION=25.02
ARG DIVEMesh_VERSION=24.12
ARG WORKDIR=/


WORKDIR ${WORKDIR}

# clone Hypre from Github and install it
RUN git clone https://github.com/hypre-space/hypre.git \
    && cd hypre/src && ./configure --prefix=/usr/local/hypre && make all -j 8 && make install
# adding paths for hypre
ENV PATH=/usr/local/hypre/include:/usr/local/hypre/lib:$PATH

# clone DIVEMesh and REEF3D from Github and make files
RUN git clone --branch ${DIVEMesh_VERSION} https://github.com/REEF3D/DIVEMesh.git \
    && cd DIVEMesh && make -j 8 && cd .. \
    && git clone --branch ${REEF3D_VERSION} https://github.com/REEF3D/REEF3D.git \
    && cd REEF3D && make -j 8

ENV REEF3D_BIN=/REEF3D/bin/REEF3D
ENV DIVEMESH_BIN=/DIVEMesh/bin/DiveMESH

ENV PATH=$REEF3D_BIN:$DIVEMESH_BIN:$PATH

COPY --from=test_env /home /home
