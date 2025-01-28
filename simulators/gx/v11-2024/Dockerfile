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
COPY --from=build /usr/lib/x86_64-linux-gnu/libm.so.6 /usr/lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libc.so.6 /usr/lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/librt.so.1 /usr/lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libdl.so.2 /usr/lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libsz.so.2 /usr/lib/x86_64-linux-gnu/libsz.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libssh.so.4 /usr/lib/x86_64-linux-gnu/libssh.so.4
COPY --from=build /usr/lib/x86_64-linux-gnu/libpsl.so.5 /usr/lib/x86_64-linux-gnu/libpsl.so.5
COPY --from=build /usr/lib/x86_64-linux-gnu/libssl.so.3 /usr/lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /usr/lib/x86_64-linux-gnu/libaec.so.0 /usr/lib/x86_64-linux-gnu/libaec.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libffi.so.8 /usr/lib/x86_64-linux-gnu/libffi.so.8
COPY --from=build /usr/lib/x86_64-linux-gnu/libmpi.so.40 /usr/lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /usr/lib/x86_64-linux-gnu/libgsl.so.27 /usr/lib/x86_64-linux-gnu/libgsl.so.27
# COPY --from=build /usr/lib/x86_64-linux-gnu/libcuda.so.1 /usr/lib/x86_64-linux-gnu/libcuda.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libcuda.so.535.183.01 /usr/lib/x86_64-linux-gnu/libcuda.so.535.183.01
COPY --from=build /usr/lib/x86_64-linux-gnu/libcurl.so.4 /usr/lib/x86_64-linux-gnu/libcurl.so.4
COPY --from=build /usr/lib/x86_64-linux-gnu/libudev.so.1 /usr/lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libidn2.so.0 /usr/lib/x86_64-linux-gnu/libidn2.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/librtmp.so.1 /usr/lib/x86_64-linux-gnu/librtmp.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libzstd.so.1 /usr/lib/x86_64-linux-gnu/libzstd.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libgmp.so.10 /usr/lib/x86_64-linux-gnu/libgmp.so.10
COPY --from=build /usr/lib/x86_64-linux-gnu/libkrb5.so.3 /usr/lib/x86_64-linux-gnu/libkrb5.so.3
COPY --from=build /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libsasl2.so.2 /usr/lib/x86_64-linux-gnu/libsasl2.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libtasn1.so.6 /usr/lib/x86_64-linux-gnu/libtasn1.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libhwloc.so.15 /usr/lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /usr/lib/x86_64-linux-gnu/libcrypto.so.3 /usr/lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /usr/lib/x86_64-linux-gnu/libnettle.so.8 /usr/lib/x86_64-linux-gnu/libnettle.so.8
COPY --from=build /usr/lib/x86_64-linux-gnu/libresolv.so.2 /usr/lib/x86_64-linux-gnu/libresolv.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libpthread.so.0 /usr/lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libgnutls.so.30 /usr/lib/x86_64-linux-gnu/libgnutls.so.30
COPY --from=build /usr/lib/x86_64-linux-gnu/libhogweed.so.6 /usr/lib/x86_64-linux-gnu/libhogweed.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libcom_err.so.2 /usr/lib/x86_64-linux-gnu/libcom_err.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libp11-kit.so.0 /usr/lib/x86_64-linux-gnu/libp11-kit.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libgslcblas.so.0 /usr/lib/x86_64-linux-gnu/libgslcblas.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libnghttp2.so.14 /usr/lib/x86_64-linux-gnu/libnghttp2.so.14
COPY --from=build /usr/lib/x86_64-linux-gnu/libldap-2.5.so.0 /usr/lib/x86_64-linux-gnu/libldap-2.5.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/liblber-2.5.so.0 /usr/lib/x86_64-linux-gnu/liblber-2.5.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libk5crypto.so.3 /usr/lib/x86_64-linux-gnu/libk5crypto.so.3
COPY --from=build /usr/lib/x86_64-linux-gnu/libkeyutils.so.1 /usr/lib/x86_64-linux-gnu/libkeyutils.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libopen-rte.so.40 /usr/lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /usr/lib/x86_64-linux-gnu/libopen-pal.so.40 /usr/lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /usr/lib/x86_64-linux-gnu/libbrotlidec.so.1 /usr/lib/x86_64-linux-gnu/libbrotlidec.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libunistring.so.2 /usr/lib/x86_64-linux-gnu/libunistring.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libnetcdf_mpi.so.19 /usr/lib/x86_64-linux-gnu/libnetcdf_mpi.so.19
COPY --from=build /usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libkrb5support.so.0 /usr/lib/x86_64-linux-gnu/libkrb5support.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 /usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libhdf5_openmpi.so.103 /usr/lib/x86_64-linux-gnu/libhdf5_openmpi.so.103
COPY --from=build /usr/lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /usr/lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /usr/lib/x86_64-linux-gnu/libhdf5_openmpi_hl.so.100 /usr/lib/x86_64-linux-gnu/libhdf5_openmpi_hl.so.100
COPY --from=build /usr/lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /usr/lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libcudart.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libcudart.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libnvJitLink.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/cuda/lib64/libnvJitLink.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublas.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublas.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/nccl/lib/libnccl.so.2 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/comm_libs/nccl/lib/libnccl.so.2
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcutensor.so.1 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcutensor.so.1
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusolver.so.11 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusolver.so.11
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublasLt.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcublasLt.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusparse.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/2023/math_libs/lib64/libcusparse.so.12

RUN apt-get update -y && \
    apt-get install -y openmpi-bin && \
    ln -s /usr/lib/x86_64-linux-gnu/libcuda.so.535.183.01 /usr/lib/x86_64-linux-gnu/libcuda.so.1