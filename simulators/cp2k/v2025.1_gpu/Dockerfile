

# Stage 1: Build
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 AS build

# Build-specific arguments
ARG CP2K_VERSION=2025.1
ARG CP2K_BRANCH=support/v${CP2K_VERSION}
ARG BUILD_JOBS=8
ARG TARGET_CPU=haswell
ARG CP2K_ROOT=/opt/cp2k
ARG TOOLCHAIN_ROOT=/toolchain

ENV FCFLAGS="-march=haswell -O3 -funroll-loops"
ENV CFLAGS="-march=haswell -O3 -funroll-loops"

# Setup CUDA environment
ENV CUDA_PATH /usr/local/cuda
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64


# Disable JIT cache as there seems to be an issue with file locking on overlayfs
# See also https://github.com/cp2k/cp2k/pull/2337
ENV CUDA_CACHE_DISABLE 1

# Install build dependencies
RUN apt-get update -qq && apt-get install -qq --no-install-recommends \
    g++ gcc gfortran openssh-client python3 libtool libtool-bin \
    bzip2 ca-certificates git make patch pkg-config unzip wget zlib1g-dev

# Clone and build CP2K
WORKDIR ${CP2K_ROOT}
RUN git clone --recursive -b ${CP2K_BRANCH} https://github.com/cp2k/cp2k.git .

# Build CP2K toolchain
WORKDIR ${CP2K_ROOT}/tools/toolchain
RUN ./install_cp2k_toolchain.sh -j ${BUILD_JOBS} \
    --install-all \
    --enable-cuda=yes \
    --gpu-ver=H100 \
    --with-deepmd=no \
    --with-libtorch=no \
    --target-cpu=${TARGET_CPU} \
    --with-cusolvermp=no \
    --with-gcc=system \
    --with-openmpi=install

# Build CP2K for target CPU native
WORKDIR /opt/cp2k
RUN /bin/bash -c -o pipefail \
    "cp ./tools/toolchain/install/arch/local_cuda.psmp ./arch/; \
     source ./tools/toolchain/install/setup; \
     make -j 8 ARCH=local_cuda VERSION=psmp"

# Collect components for installation and remove symbolic links
RUN /bin/bash -c -o pipefail \
    "mkdir -p /toolchain/install /toolchain/scripts; \
     for libdir in \$(ldd ./exe/local_cuda/cp2k.psmp | \
                      grep /opt/cp2k/tools/toolchain/install | \
                      awk '{print \$3}' | cut -d/ -f7 | \
                      sort | uniq) setup; do \
        cp -ar /opt/cp2k/tools/toolchain/install/\${libdir} /toolchain/install; \
     done; \
     cp /opt/cp2k/tools/toolchain/scripts/tool_kit.sh /toolchain/scripts; \
     unlink ./exe/local_cuda/cp2k.popt; \
     unlink ./exe/local_cuda/cp2k_shell.psmp"

# Stage 2: Installation
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 AS install

# Installation-specific arguments
ARG CP2K_ROOT=/opt/cp2k

ENV OMP_NUM_THREADS=1
ENV OMPI_MCA_btl_vader_single_copy_mechanism=none\
    OMP_STACKSIZE=16M\
    PATH=/opt/cp2k/exe/local_cuda:${PATH}

ENV FCFLAGS="-march=haswell -O3 -funroll-loops"
ENV CFLAGS="-march=haswell -O3 -funroll-loops"

# Setup CUDA environment
ENV CUDA_PATH /usr/local/cuda
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64


# Install required packages
RUN apt-get update -qq && apt-get install -qq --no-install-recommends \
    g++ gcc gfortran openssh-client python3 && rm -rf /var/lib/apt/lists/*

# Copy CP2K components from build stage
COPY --from=build ${CP2K_ROOT}/exe/local_cuda/ ${CP2K_ROOT}/exe/local_cuda/
COPY --from=build ${CP2K_ROOT}/tests/ATOM/regtest-1 /home/examples
COPY --from=build ${CP2K_ROOT}/tools/regtesting/ ${CP2K_ROOT}/tools/regtesting/
COPY --from=build ${CP2K_ROOT}/src/grid/sample_tasks/ ${CP2K_ROOT}/src/grid/sample_tasks/
COPY --from=build ${CP2K_ROOT}/data/ ${CP2K_ROOT}/data/
COPY --from=build /toolchain/ ${CP2K_ROOT}/tools/toolchain/

# Create symbolic links for binaries
RUN /bin/bash -c -o pipefail \
    "for binary in cp2k dumpdcd graph xyz2dcd; do \
        ln -sf ${CP2K_ROOT}/exe/local_cuda/${binary}.psmp /usr/local/bin/${binary}; \
    done && \
    ln -sf ${CP2K_ROOT}/exe/local_cuda/cp2k.psmp /usr/local/bin/cp2k_shell && \
    ln -sf ${CP2K_ROOT}/exe/local_cuda/cp2k.psmp /usr/local/bin/cp2k.popt"


# Create entrypoint script file
RUN printf "#!/bin/bash\n\
ulimit -c 0 -s unlimited\n\
\
export OMPI_MCA_btl_vader_single_copy_mechanism=none\n\
export OMP_STACKSIZE=16M\n\
export PATH=/opt/cp2k/exe/local:\${PATH}\n\
source /opt/cp2k/tools/toolchain/install/setup\n\
\"\$@\"" \
>/usr/local_cuda/bin/entrypoint.sh && chmod +rx /usr/local_cuda/bin/entrypoint.sh

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Configure container
WORKDIR /home
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


CMD ["cp2k.psmp"]
