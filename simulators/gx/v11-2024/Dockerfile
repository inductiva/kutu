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