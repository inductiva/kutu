FROM ubuntu:22.04 as test_env

RUN apt-get update -y; \
    apt-get install curl unzip -y; \
    curl https://storage.googleapis.com/inductiva-api-demo-files/dualsphysics-input-example.zip\ 
        --output /home/dualsphysics-input-example.zip && \
    unzip /home/dualsphysics-input-example.zip -d /home/ && \
    rm /home/dualsphysics-input-example.zip && \
    #Reduce Simulation time to 1 second
    sed -i 's/key="TimeMax" value="3"/key="TimeMax" value="1"/g' \
        /home/dualsphysics-input-example/config.xml

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Start from an image provided by NVIDIA with CUDA 11.7.
FROM ubuntu:22.04 as build

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install git and cmake.
RUN apt-get update -y \
    && apt-get install -y git cmake wget unzip

# Install Python 3.11.
RUN apt-get update -y; \
    apt-get install curl software-properties-common g++ -y; \
    add-apt-repository ppa:deadsnakes/ppa; \
    apt-get install -y python3.11 python3.11-distutils; \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11; \
    rm -f /usr/bin/python && ln -s /usr/bin/python3.11 /usr/bin/python

# Clone the DualSPHysics repository.
WORKDIR /

RUN wget -O DualSPHysics_v5.2.zip  https://storage.googleapis.com/inductiva-host-source-codes/DualSPHysics_v5.2.1.zip\
    && unzip /DualSPHysics_v5.2.zip && \
    rm -r /DualSPHysics_v5.2.zip \ 
        /DualSPHysics_v5.2/bin/windows \
        /DualSPHysics_v5.2/CHANGES.txt \
        /DualSPHysics_v5.2/examples/ \
        /DualSPHysics_v5.2/doc/ \
        /DualSPHysics_v5.2/Files_DualSPHysics_v5.2.pdf \
        /DualSPHysics_v5.2/src/VS \
        /DualSPHysics_v5.2/src/lib/vs2022/ \
        /DualSPHysics_v5.2/src_flexstruc/VS/ \
        /DualSPHysics_v5.2/src_flexstruc/lib/vs2022/ \
        /DualSPHysics_v5.2/src_extra/ \
        /DualSPHysics_v5.2/src_mphase/ 

# Build DualSPHysics.
WORKDIR /DualSPHysics_v5.2/src/source/build
RUN CC=gcc CXX=g++ cmake .. && make DualSPHysics5.2CPU_linux64


FROM ubuntu:22.04 

# COPY libgomp libraries from the build stage.
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0 /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /DualSPHysics_v5.2 /DualSPHysics_v5.2

COPY --from=test_env /home /home
# Set environment variable with path to DualSPHysics binaries.
ENV DUALSPHYSICS_BIN_DIR="/DualSPHysics_v5.2/bin/linux"

WORKDIR /
COPY ./setup.sh /setup.sh
RUN chmod +x /setup.sh && \
    /setup.sh
