FROM ubuntu:22.04 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/cans-input-example.zip -P /home/ && \
    unzip /home/cans-input-example.zip -d /home/ && \
    rm /home/cans-input-example.zip && \
    ls -l

FROM nvcr.io/nvidia/nvhpc:24.3-devel-cuda_multi-ubuntu22.04 as dev

RUN git clone --recursive --branch v2.3.4 https://github.com/CaNS-World/CaNS && \
    sed -i 's/GPU=0/GPU=1/g' CaNS/build.conf && \
    sed -i 's/FCOMP=GNU/FCOMP=NVIDIA/g' CaNS/build.conf && \
    sed -i 's/\/opt\/nvidia\/hpc_sdk\/Linux_x86_64\/2022/\/opt\/nvidia\/hpc_sdk\/Linux_x86_64\/2024/g' CaNS/configs/libs.mk && \
    sed -i 's/\/comm_libs\/hpcx\/latest\/ompi/\/comm_libs\/openmpi\/openmpi-3.1.5/g' /CaNS/dependencies/cuDecomp/configs/nvhpcsdk.conf && \
    sed -i 's/\&\& make lib -j/\&\& mkdir build \&\& cd build \&\& cmake -DCUDECOMP_ENABLE_NVSHMEM=1 .. \&\& make -j/g' /CaNS/dependencies/external.mk
    # We have problems with build because we cant add --gpus all
    # we can only do that in run
    # cd /CaNS && \
    # make libs NVHPC_HOME=/opt/nvidia/hpc_sdk/Linux_x86_64/2024 && make && \
    # cd dependencies/cuDecomp/build && \
    # make install
    # we need to copy cans to /usr/local/bin
# Disable hcoll for openmpi    
ENV OMPI_MCA_coll=^hcoll
# NCCL Debug information
ENV NCCL_DEBUG=WARN

ENV NVSHMEM_DISABLE_CUDA_VMM=1
COPY --from=test_env /home /home
