FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN curl https://storage.googleapis.com/inductiva-api-demo-files/dualsphysics-input-example.zip\ 
        --output /home/dualsphysics-input-example.zip && \
    unzip /home/dualsphysics-input-example.zip -d /home/ && \
    rm /home/dualsphysics-input-example.zip && \
    #Reduce Simulation time to 1 second
    sed -i 's/key="TimeMax" value="3"/key="TimeMax" value="1"/g' \
        /home/dualsphysics-input-example/config.xml

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Start from an image provided by NVIDIA with CUDA 11.7.
FROM inductiva/kutu:base-image_v0.1.0 as build

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

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

RUN apt-get update && apt-get install -y \
    curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    /root/.cargo/bin/cargo install splashsurf

FROM ubuntu:22.04 

# Avoid user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.cargo/bin:${PATH}"

COPY --from=build /root/.cargo/bin/splashsurf /root/.cargo/bin/splashsurf

 

# Set default python command
RUN ln -s /usr/bin/python3 /usr/bin/python

 

# COPY libgomp libraries from the build stage.
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0 /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /DualSPHysics_v5.2 /DualSPHysics_v5.2

COPY --from=test_env /home /home

RUN cp /DualSPHysics_v5.2/bin/linux/DualSPHysics5.2CPU_linux64 /DualSPHysics_v5.2/bin/linux/dualsphysics 

# Set environment variable with path to DualSPHysics binaries.
ENV DUALSPHYSICS_BIN_DIR="/DualSPHysics_v5.2/bin/linux"
ENV PATH="${DUALSPHYSICS_BIN_DIR}:${PATH}"


WORKDIR /
COPY ./setup.sh /setup.sh
RUN chmod +x /setup.sh && \
    /setup.sh
