

# Stage 1: Build
FROM ubuntu:22.04 AS build

# Build-specific arguments
ARG CP2K_VERSION=2025.1
ARG CP2K_BRANCH=support/v${CP2K_VERSION}
ARG BUILD_JOBS=8
ARG TARGET_CPU=haswell
ARG CP2K_ROOT=/opt/cp2k
ARG TOOLCHAIN_ROOT=/toolchain
# Common packages needed for both build and runtime
ARG COMMON_PACKAGES="g++ gcc gfortran openssh-client python3"

ENV FCFLAGS="-march=haswell -O3 -funroll-loops"
ENV CFLAGS="-march=haswell -O3 -funroll-loops"

# Install build dependencies
RUN apt-get update -qq && apt-get install -qq --no-install-recommends \
    ${COMMON_PACKAGES} \
    bzip2 ca-certificates git make patch pkg-config unzip wget zlib1g-dev

# Clone and build CP2K
WORKDIR ${CP2K_ROOT}
RUN git clone --recursive -b ${CP2K_BRANCH} https://github.com/cp2k/cp2k.git .

# Build CP2K toolchain
WORKDIR ${CP2K_ROOT}/tools/toolchain
RUN ./install_cp2k_toolchain.sh -j ${BUILD_JOBS} \
    --install-all \
    --enable-cuda=no \
    --target-cpu=${TARGET_CPU} \
    --with-cusolvermp=no \
    --with-gcc=system \
    --with-openmpi=install

# Build CP2K
WORKDIR ${CP2K_ROOT}
RUN /bin/bash -c -o pipefail \
    "cp ./tools/toolchain/install/arch/local.psmp ./arch/ && \
    source ./tools/toolchain/install/setup && \
    make -j ${BUILD_JOBS} ARCH=local VERSION=psmp"

# Prepare installation files
RUN /bin/bash -c -o pipefail \
    "mkdir -p /toolchain/install /toolchain/scripts; \
     for libdir in \$(ldd ./exe/local/cp2k.psmp | \
                      grep ${CP2K_ROOT}/tools/toolchain/install | \
                      awk '{print \$3}' | cut -d/ -f7 | \
                      sort | uniq) setup; do \
        cp -ar ${CP2K_ROOT}/tools/toolchain/install/\${libdir} /toolchain/install; \
     done; \
     cp ${CP2K_ROOT}/tools/toolchain/scripts/tool_kit.sh /toolchain/scripts; \
     unlink ./exe/local/cp2k.popt; \
     unlink ./exe/local/cp2k_shell.psmp"

# Stage 2: Installation
FROM ubuntu:22.04 AS install

# Installation-specific arguments
ARG CP2K_ROOT=/opt/cp2k

ENV OMP_NUM_THREADS=1
ENV OMPI_MCA_btl_vader_single_copy_mechanism=none\
    OMP_STACKSIZE=16M\
    PATH=/opt/cp2k/exe/local:${PATH}


# Install runtime dependencies
RUN apt-get update -qq && apt-get install -qq --no-install-recommends \
    g++ gcc gfortran openssh-client python3 && rm -rf /var/lib/apt/lists/*

# Copy CP2K components from build stage
COPY --from=build ${CP2K_ROOT}/exe/local/ ${CP2K_ROOT}/exe/local/
COPY --from=build ${CP2K_ROOT}/tests/ATOM/regtest-1 /home/examples
COPY --from=build ${CP2K_ROOT}/tools/regtesting/ ${CP2K_ROOT}/tools/regtesting/
COPY --from=build ${CP2K_ROOT}/src/grid/sample_tasks/ ${CP2K_ROOT}/src/grid/sample_tasks/
COPY --from=build ${CP2K_ROOT}/data/ ${CP2K_ROOT}/data/
COPY --from=build /toolchain/ ${CP2K_ROOT}/tools/toolchain/

# Create symbolic links for binaries
RUN /bin/bash -c -o pipefail \
    "for binary in cp2k dumpdcd graph xyz2dcd; do \
        ln -sf ${CP2K_ROOT}/exe/local/${binary}.psmp /usr/local/bin/${binary}; \
    done && \
    ln -sf ${CP2K_ROOT}/exe/local/cp2k.psmp /usr/local/bin/cp2k_shell && \
    ln -sf ${CP2K_ROOT}/exe/local/cp2k.psmp /usr/local/bin/cp2k.popt"


# Create entrypoint script file
RUN printf "#!/bin/bash\n\
ulimit -c 0 -s unlimited\n\
\
export OMPI_MCA_btl_vader_single_copy_mechanism=none\n\
export OMP_STACKSIZE=16M\n\
export PATH=/opt/cp2k/exe/local:\${PATH}\n\
source /opt/cp2k/tools/toolchain/install/setup\n\
\"\$@\"" \
>/usr/local/bin/entrypoint.sh && chmod +rx /usr/local/bin/entrypoint.sh

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Configure container
WORKDIR /home
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]


CMD ["cp2k.psmp"]
