FROM ubuntu:22.04 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/openfast-input-example.zip -P /home/ && \
    unzip /home/openfast-input-example.zip -d /home/ && \
    rm /home/openfast-input-example.zip && \
    ls -l

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 as build

ENV DEBIAN_FRONTEND=noninteractive TZ=America/Denver

RUN apt update -qq && \
    apt install -y software-properties-common build-essential && \
    add-apt-repository ppa:git-core/ppa -y && \
    apt install -y libblas-dev liblapack-dev \
        cmake cmake-curses-gui \
        gcc gfortran make \
        python3-pip \
        wget \
        git \
        nano

RUN pip3 install numpy

# Configure the environment
ENV FC=/usr/bin/gfortran

# Clone the project
RUN git clone --recursive --branch v3.5.2 https://github.com/openfast/openfast.git openfast
WORKDIR /openfast

# Build the project
RUN mkdir build
WORKDIR /openfast/build

# NOTE: building with optimizations on (RELEASE or RELWITHDEBINFO), the virtual machine
# will require about 6GB of memoery. Otherwise, the gfortran compiler will exit with an
# "internal error"
RUN cmake .. -DOPENMP=ON -DDOUBLE_PRECISION=ON -DCMAKE_BUILD_TYPE=Release
RUN make install

WORKDIR /openfast

# Install miniconda and ROSCO (Rosco can be used with openfast)
# This will generate /openfast/ROSCO/rosco/lib/libdiscon.so
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py312_24.1.2-0-Linux-x86_64.sh -P /tmp/

ENV PATH="/root/miniconda3/bin:${PATH}"
RUN chmod +x /tmp/Miniconda3-py312_24.1.2-0-Linux-x86_64.sh && \
    bash /tmp/Miniconda3-py312_24.1.2-0-Linux-x86_64.sh -b && \
    conda config --add channels conda-forge && \
    conda create -y --name rosco-env python=3.10 && \
    conda init bash && \
    . ~/.bashrc && \
    conda activate rosco-env && \
    git clone https://github.com/NREL/ROSCO.git && \
    cd ROSCO && \
    pip install -e .


From ubuntu:22.04

# Openfast binaries: /usr/local/bin
# ROSCO shared library: /usr/lib/x86_64-linux-gnu/libdiscon.so

Copy --from=test_env /home /home

Copy --from=build /usr/lib/x86_64-linux-gnu/libquadmath.so.0 /usr/lib/x86_64-linux-gnu/libquadmath.so.0
Copy --from=build /usr/lib/x86_64-linux-gnu/libgfortran.so.5 /usr/lib/x86_64-linux-gnu/libgfortran.so.5
Copy --from=build /usr/lib/x86_64-linux-gnu/liblapack.so.3 /usr/lib/x86_64-linux-gnu/liblapack.so.3
Copy --from=build /usr/lib/x86_64-linux-gnu/libblas.so.3 /usr/lib/x86_64-linux-gnu/libblas.so.3
Copy --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1

# Copy the binaries and shared libraries to the appropriate directories
Copy --from=build /openfast/install/bin/* /usr/local/bin/
Copy --from=build /openfast/ROSCO/rosco/lib/libdiscon.so /usr/lib/x86_64-linux-gnu/libdiscon.so
