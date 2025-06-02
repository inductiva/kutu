FROM ubuntu:22.04 as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/fds-input-example.zip -P /home/ && \
    unzip /home/fds-input-example.zip -d /home/ && \
    rm /home/fds-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Ubuntu Image
FROM ubuntu:22.04

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    make \
    wget \
    gfortran-9 &&\
    update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-9 60 &&\
    yes '' | update-alternatives --force --all

# Download openmpi and install
RUN wget https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.6.tar.gz &&\
    tar zxvf openmpi-4.1.6.tar.gz &&\
    cd /openmpi-4.1.6 &&\
    ./configure FC=gfortran-9 CC=gcc-9 --prefix=/shared/openmpi_64 --enable-mpirun-prefix-by-default --enable-mpi-fortran --enable-static --disable-shared &&\
    make -j 2 &&\
    make install &&\
    ldconfig &&\
    cd / &&\
    rm -rf openmpi-4.1.6 openmpi-4.1.6.tar.gz

ENV MPIDIST=/shared/openmpi_64
ENV PATH=$MPIDIST/bin:$PATH
ENV LD_LIBRARY_PATH=$MPIDIST/lib:$LD_LIBRARY_PATH

WORKDIR /

# Extract files to get smokeview
RUN wget https://github.com/firemodels/fds/releases/download/FDS-6.8.0/FDS-6.8.0_SMV-6.8.0_lnx.sh &&\
    printf "extract\n" | bash /FDS-6.8.0_SMV-6.8.0_lnx.sh &&\
    mkdir /opt/smokeview && \
    tar -xvzf FDS-6.8.0_SMV-6.8.0_lnx.tar.gz -C /opt/smokeview/ &&\
    rm -f FDS-6.8.0_SMV-6.8.0_lnx.tar.gz /FDS-6.8.0_SMV-6.8.0_lnx.sh &&\
    apt-get install -y \
    libx11-6 \
    libxmu6 \
    libglu1-mesa \
    libgl1-mesa-glx \
    xvfb \
    git;

#Clone fds and builds fds with openmpi for linux
RUN cd /opt &&\
    git clone https://github.com/firemodels/fds.git && \
    cd /opt/fds/Build/ompi_gnu_linux && \
    ./make_fds.sh && \
    cd .. &&\
    make clean &&\
    ln -s /opt/fds/Build/ompi_gnu_linux/fds_ompi_gnu_linux /usr/bin/fds

ENV PATH=/opt/smokeview/smvbin:$PATH

ENV DISPLAY :1
WORKDIR /

COPY --from=test_env /home /home
COPY ./smokeview.sh /smokeview.sh
RUN chmod +x /smokeview.sh

ENV OMP_NUM_THREADS=1