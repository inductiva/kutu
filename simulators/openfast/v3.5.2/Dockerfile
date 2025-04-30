FROM ubuntu:22.04 AS test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/openfast-input-example.zip -P /home/ && \
    unzip /home/openfast-input-example.zip -d /home/ && \
    rm /home/openfast-input-example.zip && \
    ls -l

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 AS build

RUN apt update && \
    apt install -y gpg-agent wget && \
    # download the key to system keyring
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list && \
    apt update && \
    apt install intel-oneapi-hpc-toolkit intel-oneapi-base-toolkit -y && \
    apt install -y \
        git && \
    # Clone Openfast repository
    git clone --recursive --branch v3.5.2 https://github.com/openfast/openfast.git openfast && \
    cd /openfast && \
    #Build Openfast with Fast.Farm
    mkdir build && \
    cd build && \
    # NOTE: building with optimizations on (RELEASE or RELWITHDEBINFO), the virtual machine
    # will require about 6GB of memoery. Otherwise, the gfortran compiler will exit with an
    # "internal error"
    cmake .. -DOPENMP=ON -DDOUBLE_PRECISION=ON -DCMAKE_BUILD_TYPE=Release -DBUILD_FASTFARM=ON && \
    make -j 4 FAST.Farm && \
    make -j 4 install && \
    cd /openfast && \
    # Compile ROSCO Controller (Rosco can be used with openfast)
    # This will generate /openfast/ROSCO/rosco/controller/build/libdiscon.so
    git clone https://github.com/NREL/ROSCO.git && \
    cd ROSCO/rosco/controller/ && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j 4 && \
    cp -a /openfast/install/bin/* /usr/local/bin/ && \
    cp -a /openfast/ROSCO/rosco/controller/build/libdiscon.so /usr/lib/x86_64-linux-gnu/libdiscon.so

# Copy test environment files
COPY --from=test_env /home /home

WORKDIR /openfast
