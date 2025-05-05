FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/cans-input-example.zip -P /home/ && \
    unzip /home/cans-input-example.zip -d /home/ && \
    rm /home/cans-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM nvcr.io/nvidia/nvhpc:25.3-devel-cuda_multi-ubuntu22.04 AS build

RUN apt-get update && apt-get install -y \
    vim git && \
    git clone --recursive --branch v2.3.4 https://github.com/CaNS-World/CaNS && \
    cd CaNS && \
    sed -i 's/GPU=0/GPU=1/; s/FCOMP=GNU/FCOMP=NVIDIA/' configs/defaults/build-default.conf && \
    sed -i 's/-gpu=cc60,cc70,cc80/-gpu=cc60,cc70,cc80,cc89,cc90,cc86/' configs/defaults/flags-default.mk && \
    make libs && \
    make -j && \
    cp -a /CaNS/run/* /usr/local/bin/

FROM nvcr.io/nvidia/nvhpc:25.3-runtime-cuda11.8-ubuntu20.04

COPY --from=test_env /home /home

COPY --from=build /CaNS/run/ /usr/local/bin/

COPY --from=build /CaNS/dependencies/cuDecomp/build/lib/libcudecomp.so /CaNS/dependencies/cuDecomp/build/lib/libcudecomp.so
COPY --from=build /CaNS/dependencies/cuDecomp/build/lib/libcudecomp_fort.so /CaNS/dependencies/cuDecomp/build/lib/libcudecomp_fort.so

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/libc.so.6 /usr/lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libm.so.6 /usr/lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libdl.so.2 /usr/lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /usr/lib/x86_64-linux-gnu/librt.so.1 /usr/lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libutil.so.1 /usr/lib/x86_64-linux-gnu/libutil.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /usr/lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libatomic.so.1 /usr/lib/x86_64-linux-gnu/libatomic.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libpthread.so.0 /usr/lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvf.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvf.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvc.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvc.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvomp.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvomp.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/cuda/lib64/libcudart.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/cuda/lib64/libcudart.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudafor.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudafor.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libacchost.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libacchost.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudafor2.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudafor2.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvhpcatm.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvhpcatm.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libaccdevaux.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libaccdevaux.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libaccdevice.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libaccdevice.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvcpumath.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvcpumath.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/libcufft.so.11 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/libcufft.so.11
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudadevice.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudadevice.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudafor_128.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libcudafor_128.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/nccl/lib/libnccl.so.2 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/nccl/lib/libnccl.so.2
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/libcutensor.so.2 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/libcutensor.so.2
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/libcublasLt.so.12 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/libcublasLt.so.12
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvhpcwrapcufft.so /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/compilers/lib/libnvhpcwrapcufft.so
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi.so.40 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi.so.40
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libopen-rte.so.40 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libopen-rte.so.40
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libopen-pal.so.40 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libopen-pal.so.40
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi_mpifh.so.40 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi_mpifh.so.40
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi_usempif08.so.40 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi_usempif08.so.40
COPY --from=build /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi_usempi_ignore_tkr.so.40 /opt/nvidia/hpc_sdk/Linux_x86_64/25.3/comm_libs/12.8/hpcx/hpcx-2.22.1/ompi/lib/libmpi_usempi_ignore_tkr.so.40


ENV LD_LIBRARY_PATH=/CaNS/dependencies/cuDecomp/build/lib/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/25.3/cuda/lib64/:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/25.3/math_libs/lib64/:$LD_LIBRARY_PATH