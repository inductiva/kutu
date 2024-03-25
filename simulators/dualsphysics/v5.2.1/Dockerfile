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

# Source: https://github.com/DualSPHysics/DualSPHysics/wiki/5.-Running-DualSPHysics
# Folder src:
# The folder source contains the source files of v5.0 (.cpp, .cu and .h). The makefile of linux and the text file for CMAKE.txt are also included in this folder.
# Visual studio (Community 2015) project for windows can be found in VS.
# The libraries (.a and .lib) necessary for compilation are included in lib.
# Folder src_extra:
# The release includes not only the source files of DualSPHysics v5.0 but also the source files of a code named “ToVTK5”. This code is provided to show how to load particle data, how to read .bi4 files and how to create .vtk or .csv files.
# Folder src_mphase:
# The source files of the of DualSPHysics_v4.0_LiquidGas and DSPH_v5.0_NNmphase are included here.
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

# Copy libgomp libraries from the build stage.
Copy --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0 /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0
Copy --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
Copy --from=build /DualSPHysics_v5.2 /DualSPHysics_v5.2

Copy --from=test_env /home /home
# Set environment variable with path to DualSPHysics binaries.
ENV DUALSPHYSICS_BIN_DIR="/DualSPHysics_v5.2/bin/linux"

WORKDIR /
COPY ./setup.sh /setup.sh
RUN chmod +x /setup.sh && \
    /setup.sh
