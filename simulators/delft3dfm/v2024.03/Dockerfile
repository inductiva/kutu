# Source: https://github.com/veethahavya-CU-cz/delft3dfm_dockerized/blob/main/ubuntu-20.04_intel_basic/Dockerfile
FROM intel/oneapi-hpckit:devel-ubuntu20.04 AS build

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

# Install all build dependencies in a single layer
RUN apt-get -y update && apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
        patchelf subversion python3-distutils unzip \
        m4 zlib1g zlib1g-dev ruby uuid uuid-dev curl libcurl4 libcurl4-openssl-dev \
        expat libexpat1-dev autoconf libtool bison flex environment-modules \
        libproj-dev libgtest-dev libgdal-dev libboost-all-dev && \
    rm -rf /var/lib/apt/lists/*

# Install modern cmake required by Delft3D FM build system
RUN wget https://github.com/Kitware/CMake/releases/download/v3.30.4/cmake-3.30.4-linux-x86_64.sh -O /tmp/cmake.sh && \
    chmod +x /tmp/cmake.sh && \
    mkdir -p /opt/cmake && \
    /tmp/cmake.sh --skip-license --prefix=/opt/cmake && \
    ln -sf /opt/cmake/bin/cmake /usr/local/bin/cmake && \
    rm /tmp/cmake.sh


## setting up to compile and install dependencies
RUN mkdir -p /home/delft3dfm_compile/dependencies
WORKDIR /home/delft3dfm_compile/dependencies

# install PETSc (built with Intel compilers for module compatibility)
RUN wget https://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.19.4.tar.gz -O petsc-3.19.4.tar.gz && \
    tar -xf petsc-3.19.4.tar.gz
WORKDIR /home/delft3dfm_compile/dependencies/petsc-3.19.4
RUN /usr/bin/python3 ./configure \
        --prefix=/usr/local/petsc-3.19 \
        --with-cc=mpiicc \
        --with-cxx=mpiicpc \
        --with-fc=mpiifort \
        --with-debugging=0 \
        --with-shared-libraries=1 \
        --with-x=0 \
        --download-f2cblaslapack=1 \
        --download-metis=1 \
        --download-parmetis=1 \
    || (cat configure.log && exit 1)
RUN make all && make install
ENV PETSC_DIR=/usr/local/petsc-3.19
ENV PETSC_ARCH=""
ENV PKG_CONFIG_PATH=/usr/local/petsc-3.19/lib/pkgconfig:${PKG_CONFIG_PATH}

# reset workdir for remaining dependencies
WORKDIR /home/delft3dfm_compile/dependencies

# install hdf5-1.10.6 with parallel io support
RUN wget github.com/HDFGroup/hdf5/archive/refs/tags/hdf5-1_10_6.tar.gz && tar -xf hdf5-1_10_6.tar.gz
WORKDIR /home/delft3dfm_compile/dependencies/hdf5-hdf5-1_10_6
RUN ./configure CC=mpiicc CXX=mpiicxx FC=mpiifort --enable-parallel --enable-shared --prefix=/usr/local CFLAGS="-m64 -diag-disable=10441"
RUN make install

# install netcdf c-libs with parallel io support
WORKDIR /home/delft3dfm_compile/dependencies
RUN wget github.com/Unidata/netcdf-c/archive/refs/tags/v4.6.1.tar.gz -O netcdf-c-4.6.1.tar.gz && tar -xf netcdf-c-4.6.1.tar.gz
WORKDIR /home/delft3dfm_compile/dependencies/netcdf-c-4.6.1
RUN ./configure CC=mpiicc CXX=mpiicxx FC=mpiifort --enable-parallel --enable-shared --prefix=/usr/local --enable-fortran --enable-remote-fortran-bootstrap --disable-dap-remote-tests CFLAGS="-m64 -diag-disable=10441"
RUN make install

## install netcdf fortran-libs
WORKDIR /home/delft3dfm_compile/dependencies
RUN wget github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.5.0.tar.gz -O netcdf-fortran-4.5.0.tar.gz && tar -xf netcdf-fortran-4.5.0.tar.gz
WORKDIR /home/delft3dfm_compile/dependencies/netcdf-fortran-4.5.0
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}
RUN ./configure CC=mpiicc CXX=mpiicxx FC=mpiifort F77=mpiifort --prefix=/usr/local --disable-fortran-type-check CPPFLAGS="-I/usr/local/include" LDFLAGS="-L/usr/local/lib" CFLAGS="-m64 -diag-disable=10441" --enable-shared --host=x86_64-pc-linux
RUN make install

# Install ESMF (required for D-Waves grid regridding)
WORKDIR /home/delft3dfm_compile/dependencies
RUN wget -q https://github.com/esmf-org/esmf/archive/refs/tags/v8.6.1.tar.gz -O esmf-8.6.1.tar.gz && \
    tar -xf esmf-8.6.1.tar.gz
WORKDIR /home/delft3dfm_compile/dependencies/esmf-8.6.1
ENV ESMF_DIR=/home/delft3dfm_compile/dependencies/esmf-8.6.1
ENV ESMF_INSTALL_PREFIX=/usr/local/esmf
ENV ESMF_COMPILER=intel
ENV ESMF_COMM=intelmpi
ENV ESMF_NETCDF=nc-config
RUN make -j$(nproc) && make install
# ESMF binary is at /usr/local/esmf/bin/binO/Linux.intel.64.intelmpi.default/ESMF_RegridWeightGen

# clean up src of dependencies
RUN rm -rf /home/delft3dfm_compile/dependencies


## Compiling Delft3D FM
RUN curl -L -o /tmp/Delft3D-DIMRset_2026.01.zip https://storage.googleapis.com/inductiva-api-demo-files/Delft3D-DIMRset_2026.01.zip && \
    unzip /tmp/Delft3D-DIMRset_2026.01.zip -d / && \
    mv /Delft3D-DIMRset_2026.01 /delft3dfm && \
    rm /tmp/Delft3D-DIMRset_2026.01.zip
WORKDIR /delft3dfm

# Patch: Make ESMF optional at cmake configure time (will be available at runtime)
RUN sed -i 's/ESMF_RegridWeightGen REQUIRED/ESMF_RegridWeightGen/' \
    /delft3dfm/src/engines_gpl/wave/packages/wave/wave_exe.cmake

# Build fm-suite first (D-WAQ, DIMR, D-Waves, DRR, tools)
RUN export NUM_JOBS=$(nproc) && \
    export CC=mpiicc CXX=mpiicpc FC=mpiifort && \
    export LDFLAGS="-L/opt/intel/oneapi/mpi/2021.6.0/lib -lmpifort" && \
    mkdir -p build_fmsuite && \
    cd build_fmsuite && \
    /opt/cmake/bin/cmake ../src/cmake -G "Unix Makefiles" -B "." \
        -D CONFIGURATION_TYPE="fm-suite" \
        -D CMAKE_BUILD_TYPE=Release \
        -D CMAKE_INSTALL_PREFIX=/opt/delft3dfm \
        -D CMAKE_EXE_LINKER_FLAGS="-L/opt/intel/oneapi/mpi/2021.6.0/lib -lmpifort" && \
    make -j${NUM_JOBS} && \
    make install || true && \
    mkdir -p /opt/delft3dfm/bin /opt/delft3dfm/lib /opt/delft3dfm/scripts && \
    find /delft3dfm/build_fmsuite -type f -executable \( -name "delwaq" -o -name "wave_exe" -o -name "dimr" -o -name "dfmoutput" -o -name "delpar" -o -name "rr" -o -name "maptonetcdf" -o -name "swan_mpi" -o -name "swan_omp" \) -exec cp {} /opt/delft3dfm/bin/ \; && \
    find /delft3dfm/build_fmsuite -name "*.so" -exec cp {} /opt/delft3dfm/lib/ \; && \
    cp /usr/local/esmf/bin/binO/Linux.intel.64.intelmpi.default/ESMF_RegridWeightGen /opt/delft3dfm/bin/ && \
    cp /delft3dfm/src/third_party_open/esmf/lnx64/scripts/ESMF_RegridWeightGen_in_Delft3D-WAVE.sh /opt/delft3dfm/scripts/ && \
    cp /delft3dfm/src/third_party_open/swan/scripts/swan.sh /opt/delft3dfm/scripts/ && \
    chmod +x /opt/delft3dfm/scripts/*.sh && \
    test -f /opt/delft3dfm/bin/delwaq || (echo "ERROR: delwaq not found after build!" && find /delft3dfm/build_fmsuite -name "*delwaq*" -ls && exit 1) && \
    rm -rf /delft3dfm/build_fmsuite

# Build dflowfm CLI separately
RUN export NUM_JOBS=$(nproc) && \
    export CC=mpiicc CXX=mpiicpc FC=mpiifort && \
    export LDFLAGS="-L/opt/intel/oneapi/mpi/2021.6.0/lib -lmpifort" && \
    mkdir -p build_dflowfm && \
    cd build_dflowfm && \
    /opt/cmake/bin/cmake ../src/cmake -G "Unix Makefiles" -B "." \
        -D CONFIGURATION_TYPE="dflowfm" \
        -D CMAKE_BUILD_TYPE=Release \
        -D CMAKE_INSTALL_PREFIX=/opt/delft3dfm \
        -D CMAKE_EXE_LINKER_FLAGS="-L/opt/intel/oneapi/mpi/2021.6.0/lib -lmpifort" && \
    make -j${NUM_JOBS} && \
    make install || true && \
    find /delft3dfm/build_dflowfm -type f -executable -name "dflowfm" -exec cp {} /opt/delft3dfm/bin/ \; && \
    find /delft3dfm/build_dflowfm -type f -executable -name "dfm_volume_tool" -exec cp {} /opt/delft3dfm/bin/ \; && \
    rm -rf /delft3dfm/build_dflowfm

ENV PATH=/opt/delft3dfm/bin:${PATH}
ENV LD_LIBRARY_PATH=/opt/delft3dfm/lib:${LD_LIBRARY_PATH}

FROM ubuntu:20.04

# Install runtime dependencies
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends libboost-filesystem1.71.0 libboost-system1.71.0 libboost-date-time1.71.0 && \
    rm -rf /var/lib/apt/lists/*

# Copy all files from build stage
# Delft3D FM binaries and libraries
COPY --from=build /opt/delft3dfm /opt/delft3dfm

# Intel OneAPI components
COPY --from=build /opt/intel/oneapi/etc /opt/intel/oneapi/etc
COPY --from=build /opt/intel/oneapi/mpi /opt/intel/oneapi/mpi
COPY --from=build /opt/intel/oneapi/licensing /opt/intel/oneapi/licensing
COPY --from=build /opt/intel/oneapi/setvars.sh /opt/intel/oneapi/setvars.sh
COPY --from=build /opt/intel/oneapi/modulefiles-setup.sh /opt/intel/oneapi/modulefiles-setup.sh
COPY --from=build /opt/intel/oneapi/readme-get-started-linux-hpc-kit.html /opt/intel/oneapi/readme-get-started-linux-hpc-kit.html
COPY --from=build /opt/intel/oneapi/readme-get-started-linux-base-kit.html /opt/intel/oneapi/readme-get-started-linux-base-kit.html

# Dependencies
COPY --from=build /usr/local/petsc-3.19 /usr/local/petsc-3.19
COPY --from=build /usr/local/esmf /usr/local/esmf
COPY --from=build /usr/local/lib/libhdf5.so.103 /usr/local/lib/libhdf5.so.103
COPY --from=build /usr/local/lib/libhdf5_hl.so.100 /usr/local/lib/libhdf5_hl.so.100
COPY --from=build /usr/local/lib/libnetcdf.so.13 /usr/local/lib/libnetcdf.so.13
COPY --from=build /usr/local/lib/libnetcdff.so.7 /usr/local/lib/libnetcdff.so.7

# System libraries
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libgomp.so.1 /lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libffi.so.7 /lib/x86_64-linux-gnu/libffi.so.7
COPY --from=build /lib/x86_64-linux-gnu/libresolv.so.2 /lib/x86_64-linux-gnu/libresolv.so.2
COPY --from=build /lib/x86_64-linux-gnu/libcrypt.so.1 /lib/x86_64-linux-gnu/libcrypt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libexpat.so.1 /lib/x86_64-linux-gnu/libexpat.so.1

# Network/SSL libraries
COPY --from=build /lib/x86_64-linux-gnu/libcurl.so.4 /lib/x86_64-linux-gnu/libcurl.so.4
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.1.1 /lib/x86_64-linux-gnu/libssl.so.1.1
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.1.1 /lib/x86_64-linux-gnu/libcrypto.so.1.1
COPY --from=build /lib/x86_64-linux-gnu/libssh.so.4 /lib/x86_64-linux-gnu/libssh.so.4
COPY --from=build /lib/x86_64-linux-gnu/libpsl.so.5 /lib/x86_64-linux-gnu/libpsl.so.5
COPY --from=build /lib/x86_64-linux-gnu/libnghttp2.so.14 /lib/x86_64-linux-gnu/libnghttp2.so.14
COPY --from=build /lib/x86_64-linux-gnu/libbrotlidec.so.1 /lib/x86_64-linux-gnu/libbrotlidec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libbrotlicommon.so.1 /lib/x86_64-linux-gnu/libbrotlicommon.so.1

# Kerberos/Authentication libraries
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.3 /lib/x86_64-linux-gnu/libkrb5.so.3
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.26 /lib/x86_64-linux-gnu/libkrb5.so.26
COPY --from=build /lib/x86_64-linux-gnu/libkrb5support.so.0 /lib/x86_64-linux-gnu/libkrb5support.so.0
COPY --from=build /lib/x86_64-linux-gnu/libk5crypto.so.3 /lib/x86_64-linux-gnu/libk5crypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libgssapi.so.3 /lib/x86_64-linux-gnu/libgssapi.so.3
COPY --from=build /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /lib/x86_64-linux-gnu/libgssapi_krb5.so.2
COPY --from=build /lib/x86_64-linux-gnu/libhx509.so.5 /lib/x86_64-linux-gnu/libhx509.so.5
COPY --from=build /lib/x86_64-linux-gnu/libheimbase.so.1 /lib/x86_64-linux-gnu/libheimbase.so.1
COPY --from=build /lib/x86_64-linux-gnu/libheimntlm.so.0 /lib/x86_64-linux-gnu/libheimntlm.so.0
COPY --from=build /lib/x86_64-linux-gnu/libroken.so.18 /lib/x86_64-linux-gnu/libroken.so.18
COPY --from=build /lib/x86_64-linux-gnu/libwind.so.0 /lib/x86_64-linux-gnu/libwind.so.0
COPY --from=build /lib/x86_64-linux-gnu/libhcrypto.so.4 /lib/x86_64-linux-gnu/libhcrypto.so.4

# LDAP libraries
COPY --from=build /lib/x86_64-linux-gnu/liblber-2.4.so.2 /lib/x86_64-linux-gnu/liblber-2.4.so.2
COPY --from=build /lib/x86_64-linux-gnu/libldap_r-2.4.so.2 /lib/x86_64-linux-gnu/libldap_r-2.4.so.2
COPY --from=build /lib/x86_64-linux-gnu/libsasl2.so.2 /lib/x86_64-linux-gnu/libsasl2.so.2

# Crypto/Encoding libraries
COPY --from=build /lib/x86_64-linux-gnu/libgmp.so.10 /lib/x86_64-linux-gnu/libgmp.so.10
COPY --from=build /lib/x86_64-linux-gnu/libidn2.so.0 /lib/x86_64-linux-gnu/libidn2.so.0
COPY --from=build /lib/x86_64-linux-gnu/libunistring.so.2 /lib/x86_64-linux-gnu/libunistring.so.2
COPY --from=build /lib/x86_64-linux-gnu/libasn1.so.8 /lib/x86_64-linux-gnu/libasn1.so.8
COPY --from=build /lib/x86_64-linux-gnu/libtasn1.so.6 /lib/x86_64-linux-gnu/libtasn1.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgnutls.so.30 /lib/x86_64-linux-gnu/libgnutls.so.30
COPY --from=build /lib/x86_64-linux-gnu/libhogweed.so.5 /lib/x86_64-linux-gnu/libhogweed.so.5
COPY --from=build /lib/x86_64-linux-gnu/libnettle.so.7 /lib/x86_64-linux-gnu/libnettle.so.7
COPY --from=build /lib/x86_64-linux-gnu/libp11-kit.so.0 /lib/x86_64-linux-gnu/libp11-kit.so.0
COPY --from=build /lib/x86_64-linux-gnu/libcom_err.so.2 /lib/x86_64-linux-gnu/libcom_err.so.2
COPY --from=build /lib/x86_64-linux-gnu/libkeyutils.so.1 /lib/x86_64-linux-gnu/libkeyutils.so.1
COPY --from=build /lib/x86_64-linux-gnu/libuuid.so.1 /lib/x86_64-linux-gnu/libuuid.so.1
COPY --from=build /lib/x86_64-linux-gnu/librtmp.so.1 /lib/x86_64-linux-gnu/librtmp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libsqlite3.so.0 /lib/x86_64-linux-gnu/libsqlite3.so.0

# Intel MPI libraries
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//lib/libmpicxx.so.12 /opt/intel/oneapi/mpi/2021.6.0//lib/libmpicxx.so.12
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//lib/libmpifort.so.12 /opt/intel/oneapi/mpi/2021.6.0//lib/libmpifort.so.12
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//lib/release/libmpi.so.12 /opt/intel/oneapi/mpi/2021.6.0//lib/release/libmpi.so.12
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//libfabric/lib/libfabric.so.1 /opt/intel/oneapi/mpi/2021.6.0//libfabric/lib/libfabric.so.1

# Intel compiler runtime libraries
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libimf.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libimf.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirc.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirc.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirng.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirng.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libsvml.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libsvml.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libiomp5.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libiomp5.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libintlc.so.5 /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libintlc.so.5
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifport.so.5 /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifport.so.5
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifcoremt.so.5 /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifcoremt.so.5

# Intel runtime libraries
COPY --from=build /lib/x86_64-linux-gnu/libze_loader.so.1 /lib/x86_64-linux-gnu/libze_loader.so.1

# Copy OpenMP library to delft3dfm lib directory for RTC component (fixes missing __kmpc_global_thread_num symbol)
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libiomp5.so /opt/delft3dfm/lib/libiomp5.so

# Copy D-WAQ process library and examples
COPY --from=build /delft3dfm/src/engines_gpl/waq/resources/process_lib /opt/delft3dfm/share/delft3d
COPY --from=build /delft3dfm/examples/dflowfm /home/examples/dflowfm
COPY --from=build /delft3dfm/examples/delft3d4 /home/examples/delft3d4

# Copy test script
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH=/opt/delft3dfm/bin:/opt/delft3dfm/scripts:/usr/local/esmf/bin:/opt/delft3dfm/lnx64/swan/scripts/:/opt/delft3dfm/lnx64/swan/bin/:/opt/intel/oneapi/mpi/2021.6.0//bin:${PATH}
ENV LD_LIBRARY_PATH=/opt/delft3dfm/lib:/usr/local/petsc-3.19/lib:/usr/local/lib:/usr/local/esmf/lib/libO/Linux.intel.64.intelmpi.default:/opt/intel/oneapi/vpl/2022.1.0/lib:/opt/intel/oneapi/tbb/2021.6.0/env/../lib/intel64/gcc4.8:/opt/intel/oneapi/mpi/2021.6.0//libfabric/lib:/opt/intel/oneapi/mpi/2021.6.0//lib/release:/opt/intel/oneapi/mpi/2021.6.0//lib:/opt/intel/oneapi/mkl/2022.1.0/lib/intel64:/opt/intel/oneapi/itac/2021.6.0/slib:/opt/intel/oneapi/ippcp/2021.6.0/lib/intel64:/opt/intel/oneapi/ipp/2021.6.0/lib/intel64:/opt/intel/oneapi/dnnl/2022.1.0/cpu_dpcpp_gpu_dpcpp/lib:/opt/intel/oneapi/debugger/2021.6.0/gdb/intel64/lib:/opt/intel/oneapi/debugger/2021.6.0/libipt/intel64/lib:/opt/intel/oneapi/debugger/2021.6.0/dep/lib:/opt/intel/oneapi/dal/2021.6.0/lib/intel64:/opt/intel/oneapi/compiler/2022.1.0/linux/lib:/opt/intel/oneapi/compiler/2022.1.0/linux/lib/x64:/opt/intel/oneapi/compiler/2022.1.0/linux/lib/oclfpga/host/linux64/lib:/opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin:/opt/intel/oneapi/ccl/2021.6.0/lib/cpu_gpu_dpcpp:/opt/delft3dfm/lnx64/flow2d3d/bin/
ENV LD_PRELOAD=/opt/delft3dfm/lib/libiomp5.so
ENV LIBRARY_PATH=/opt/intel/oneapi/mpi/2021.6.0//libfabric/lib:/opt/intel/oneapi/mpi/2021.6.0//lib/release:/opt/intel/oneapi/mpi/2021.6.0//lib
ENV CPATH=/opt/intel/oneapi/mpi/2021.6.0//include
ENV PKG_CONFIG_PATH=/opt/intel/oneapi/mpi/2021.6.0/lib/pkgconfig
ENV CLASSPATH=/opt/intel/oneapi/mpi/2021.6.0//lib/mpi.jar
ENV VT_MPI=impi4
ENV VT_ADD_LIBS="-ldwarf -lelf -lvtunwind -lm -lpthread"
ENV IPP_TARGET_ARCH=intel64
ENV ONEAPI_ROOT=/opt/intel/oneapi
ENV I_MPI_ROOT=/opt/intel/oneapi/mpi/2021.6.0
ENV FI_PROVIDER_PATH=/opt/intel/oneapi/mpi/2021.6.0//libfabric/lib/prov:/usr/lib64/libfabric
ENV ACL_BOARD_VENDOR_PATH=/opt/Intel/OpenCLFPGA/oneAPI/Boards
ENV LESSOPEN="| /usr/bin/lesspipe %s"
ENV LESSCLOSE="/usr/bin/lesspipe %s %s"
ENV D3D_HOME=/opt/delft3dfm/
ENV ARCH=lnx64
ENV PROC_DEF_DIR=/opt/delft3dfm/share/delft3d