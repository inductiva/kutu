FROM ubuntu:22.04 as test_env

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
FROM ubuntu:22.04


# install required dependencies
RUN apt-get update --fix-missing
RUN apt-get -y install git cmake build-essential gfortran wget



WORKDIR /
RUN wget https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.6.tar.gz
RUN apt-get install -y build-essential
RUN tar zxvf openmpi-4.1.6.tar.gz
WORKDIR /openmpi-4.1.6
RUN ./configure --prefix=/usr/local
RUN make all
RUN make install
RUN ldconfig

WORKDIR /

# clone Hypre from Github and install it
RUN git clone https://github.com/hypre-space/hypre.git
RUN cd hypre/src && ./configure --prefix=/usr/local/hypre && make all -j 8 && make install
# adding paths for hypre
RUN export PATH=/usr/local/hypre/include:/usr/local/hypre/lib:$PATH

# clone DIVEMesh and REEF3D from Github and make files
RUN git clone https://github.com/REEF3D/DIVEMesh.git
RUN cd DIVEMesh && make -j 8 && cd ..
RUN git clone https://github.com/REEF3D/REEF3D.git
RUN cd REEF3D && make -j 8

ENV REEF3D_BIN=/REEF3D/bin/REEF3D
ENV DIVEMESH_BIN=/DIVEMesh/bin/DiveMESH

RUN echo "export PATH=${DIVEMESH_HOME}:${REEF3D_HOME}:$PATH" >> ~/.bashrc

COPY --from=test_env /home /home
