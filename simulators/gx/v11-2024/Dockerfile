FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/gx-input-example.zip -P /home/ && \
    unzip /home/gx-input-example.zip -d /home/ && \
    rm /home/gx-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04 as build

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
COPY --from=build /gx/gx /bin/gx

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libcudart.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libcudart.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libnvJitLink.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libnvJitLink.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublas.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublas.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/nccl/lib/libnccl.so.2 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/nccl/lib/libnccl.so.2
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcutensor.so.1 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcutensor.so.1
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusolver.so.11 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusolver.so.11
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublasLt.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublasLt.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusparse.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusparse.so.12

COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/mpi/bin /opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/mpi/bin
#For GX and NVIDIA HPC SDK
ENV LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/nccl/lib
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64
ENV PATH="$PATH:/opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/mpi/bin"

COPY --from=test_env /home /home

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean