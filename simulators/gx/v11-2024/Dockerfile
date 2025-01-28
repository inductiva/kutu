FROM inductiva/kutu:base-image_v0.1.0 as test_env

# RUN wget https://storage.googleapis.com/inductiva-api-demo-files/amr-wind-input-example.zip -P /home/ && \
#     unzip /home/amr-wind-input-example.zip -d /home/ && \
#     rm /home/amr-wind-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 as build

ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

#For GX and NVIDIA HPC SDK
ENV LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/nccl/lib
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64
ENV PATH="$PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/mpi/bin"
ENV GK_SYSTEM='gcpa2'

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt install curl -y && \
    curl https://developer.download.nvidia.com/hpc-sdk/ubuntu/DEB-GPG-KEY-NVIDIA-HPC-SDK | gpg --dearmor -o  /usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/nvidia-hpcsdk-archive-keyring.gpg] https://developer.download.nvidia.com/hpc-sdk/ubuntu/amd64 /' | tee /etc/apt/sources.list.d/nvhpc.list && \
    apt-get update -y && \
    apt-get install -y libhdf5-mpi-dev libnetcdf-mpi-dev libgsl-dev nvhpc-23-11 ubuntu-drivers-common wget git && \ 
    wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh && \
    bash Anaconda3-2024.02-1-Linux-x86_64.sh -b -p /opt/conda
# Add Conda to the PATH
ENV PATH="/opt/conda/bin:$PATH"

RUN source ~/.bashrc && \
    conda create -n gxenv python=3.11 numpy matplotlib scipy netCDF4 sphinx sphinx_rtd_theme

SHELL ["conda", "run", "-n", "gxenv", "/bin/bash", "-c"]

RUN git clone https://bitbucket.org/gyrokinetics/gx /gx && \
    cd /gx && \
    make

FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

COPY --from=test_env /home /home
COPY --from=build /gx/gx /gx/gx

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023 /opt/nvidia/hpc_sdk/Linux_x86_64/2023

RUN apt-get update -y && \
    apt-get install -y openmpi-bin && \
    ln -s /usr/lib/x86_64-linux-gnu/libcuda.so.535.183.01 /usr/lib/x86_64-linux-gnu/libcuda.so.1