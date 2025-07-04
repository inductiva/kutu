FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/delft3d-input-example.zip -P /home/ && \
    unzip /home/delft3d-input-example.zip -d /home/ && \
    rm /home/delft3d-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

#Source https://github.com/veethahavya-CU-cz/delft3dfm_dockerized/blob/main/ubuntu-20.04_intel_basic/Dockerfile
FROM intel/oneapi-hpckit:devel-ubuntu20.04 as build

ENV DEBIAN_FRONTEND=noninteractive

SHELL ["/bin/bash", "-c"]

COPY --from=test_env /home /home

# update the system
RUN apt-get -y update && apt list --upgradable && apt-get -y upgrade && \
    apt-get install subversion -y && \
    svn checkout https://svn.oss.deltares.nl/repos/delft3d/branches/releases/7545/ delft3d

# install dependencies from package manager - apt
RUN apt-get install -y m4 zlib1g zlib1g-dev ruby uuid uuid-dev curl libcurl4 libcurl4-openssl-dev expat libexpat1-dev autoconf libtool bison flex environment-modules


## setting up to compile and install dependencies
RUN mkdir -p /home/delft3dfm_compile/dependencies
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

# clean up src of dependencies
RUN rm -rf /home/delft3dfm_compile/dependencies


## compiling delft3dfm
# copy the zipped delft3dfm source code into the container
WORKDIR /delft3d/src/

# copy missing files: fix for known issue
#RUN cp third_party_open/swan/src/*.[fF]* third_party_open/swan/swan_mpi && cp third_party_open/swan/src/*.[fF]* third_party_open/swan/swan_omp

# configure the build
RUN ./autogen.sh && ./configure --with-netcdf --with-mpi CC=icc CXX=icpc FC=ifort MPICXX=mpiicpc F77=ifort MPIF77=mpiifort MPIFC=mpiifort CPPFLAGS="-I/usr/local/include" CFLAGS="-m64 -diag-disable=10441" NETCDF_CFLAGS="-I/usr/local/include" NETCDF_LIBS="-L/usr/local/lib -lnetcdf" --prefix=/opt/delft3dfm

# build
RUN source /etc/profile.d/modules.sh && \
    CC=icc \
    CXX=icpc \
    FC=ifort \
    MPICXX=mpiicpc \
    F77=ifort \
    MPIF77=mpiifort \
    MPIFC=mpiifort \
    CPPFLAGS="-I/usr/local/include" \
    CFLAGS="-m64 -xCORE-AVX2 -diag-disable=10441" \
    CXXFLAGS="-m64 -xCORE-AVX2 -diag-disable=10441" \
    FFLAGS="-m64 -xCORE-AVX2" \
    make ds-install

ENV PATH=/opt/delft3dfm/bin:${PATH}
ENV LD_LIBRARY_PATH=/opt/delft3dfm/lib:${LD_LIBRARY_PATH}

FROM ubuntu:20.04

#Copy only needed things from oneapi
COPY --from=build /opt/delft3dfm /opt/delft3dfm
COPY --from=build /opt/intel/oneapi/etc /opt/intel/oneapi/etc
COPY --from=build /opt/intel/oneapi/mpi /opt/intel/oneapi/mpi
COPY --from=build /opt/intel/oneapi/licensing /opt/intel/oneapi/licensing
COPY --from=build /opt/intel/oneapi/setvars.sh /opt/intel/oneapi/setvars.sh
COPY --from=build /opt/intel/oneapi/modulefiles-setup.sh /opt/intel/oneapi/modulefiles-setup.sh
COPY --from=build /opt/intel/oneapi/readme-get-started-linux-hpc-kit.html /opt/intel/oneapi/readme-get-started-linux-hpc-kit.html
COPY --from=build /opt/intel/oneapi/readme-get-started-linux-base-kit.html /opt/intel/oneapi/readme-get-started-linux-base-kit.html

#Set env vars
ENV PATH=/opt/delft3dfm/bin:/opt/delft3dfm/lnx64/swan/scripts/:/opt/delft3dfm/lnx64/swan/bin/:${PATH}
ENV PATH=/opt/intel/oneapi/mpi/2021.6.0//bin:${PATH}
ENV VT_MPI=impi4
ENV IPP_TARGET_ARCH=intel64
ENV LESSOPEN="| /usr/bin/lesspipe %s"
ENV ONEAPI_ROOT=/opt/intel/oneapi
ENV LESSCLOSE="/usr/bin/lesspipe %s %s"
ENV CPATH=/opt/intel/oneapi/mpi/2021.6.0//include
ENV I_MPI_ROOT=/opt/intel/oneapi/mpi/2021.6.0
ENV VT_ADD_LIBS="-ldwarf -lelf -lvtunwind -lm -lpthread"
ENV CLASSPATH=/opt/intel/oneapi/mpi/2021.6.0//lib/mpi.jar
ENV PKG_CONFIG_PATH=/opt/intel/oneapi/mpi/2021.6.0/lib/pkgconfig
ENV ACL_BOARD_VENDOR_PATH=/opt/Intel/OpenCLFPGA/oneAPI/Boards
ENV FI_PROVIDER_PATH=/opt/intel/oneapi/mpi/2021.6.0//libfabric/lib/prov:/usr/lib64/libfabric
ENV LIBRARY_PATH=/opt/intel/oneapi/mpi/2021.6.0//libfabric/lib:/opt/intel/oneapi/mpi/2021.6.0//lib/release:/opt/intel/oneapi/mpi/2021.6.0//lib
ENV LD_LIBRARY_PATH=/opt/delft3dfm/lib:/usr/local/lib:/opt/intel/oneapi/vpl/2022.1.0/lib:/opt/intel/oneapi/tbb/2021.6.0/env/../lib/intel64/gcc4.8:/opt/intel/oneapi/mpi/2021.6.0//libfabric/lib:/opt/intel/oneapi/mpi/2021.6.0//lib/release:/opt/intel/oneapi/mpi/2021.6.0//lib:/opt/intel/oneapi/mkl/2022.1.0/lib/intel64:/opt/intel/oneapi/itac/2021.6.0/slib:/opt/intel/oneapi/ippcp/2021.6.0/lib/intel64:/opt/intel/oneapi/ipp/2021.6.0/lib/intel64:/opt/intel/oneapi/dnnl/2022.1.0/cpu_dpcpp_gpu_dpcpp/lib:/opt/intel/oneapi/debugger/2021.6.0/gdb/intel64/lib:/opt/intel/oneapi/debugger/2021.6.0/libipt/intel64/lib:/opt/intel/oneapi/debugger/2021.6.0/dep/lib:/opt/intel/oneapi/dal/2021.6.0/lib/intel64:/opt/intel/oneapi/compiler/2022.1.0/linux/lib:/opt/intel/oneapi/compiler/2022.1.0/linux/lib/x64:/opt/intel/oneapi/compiler/2022.1.0/linux/lib/oclfpga/host/linux64/lib:/opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin:/opt/intel/oneapi/ccl/2021.6.0/lib/cpu_gpu_dpcpp:/opt/delft3dfm/lnx64/flow2d3d/bin/
ENV D3D_HOME=/opt/delft3dfm/
ENV ARCH=lnx64

#Intel MPI dependencies
COPY --from=build /lib/x86_64-linux-gnu/libgomp.so.1 /lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libze_loader.so.1 /lib/x86_64-linux-gnu/libze_loader.so.1
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//libfabric/lib/libfabric.so.1 /opt/intel/oneapi/mpi/2021.6.0//libfabric/lib/libfabric.so.1

#Delft3D dependencies
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /usr/local/lib/libhdf5.so.103 /usr/local/lib/libhdf5.so.103
COPY --from=build /usr/local/lib/libnetcdf.so.13 /usr/local/lib/libnetcdf.so.13
COPY --from=build /usr/local/lib/libnetcdff.so.7 /usr/local/lib/libnetcdff.so.7
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
COPY --from=build /usr/local/lib/libhdf5_hl.so.100 /usr/local/lib/libhdf5_hl.so.100
COPY --from=build /lib/x86_64-linux-gnu/libffi.so.7 /lib/x86_64-linux-gnu/libffi.so.7
COPY --from=build /lib/x86_64-linux-gnu/libpsl.so.5 /lib/x86_64-linux-gnu/libpsl.so.5
COPY --from=build /lib/x86_64-linux-gnu/libssh.so.4 /lib/x86_64-linux-gnu/libssh.so.4
COPY --from=build /opt/delft3dfm/lib/libdelwaq.so.0 /opt/delft3dfm/lib/libdelwaq.so.0
COPY --from=build /lib/x86_64-linux-gnu/libasn1.so.8 /lib/x86_64-linux-gnu/libasn1.so.8
COPY --from=build /lib/x86_64-linux-gnu/libcurl.so.4 /lib/x86_64-linux-gnu/libcurl.so.4
COPY --from=build /lib/x86_64-linux-gnu/libgmp.so.10 /lib/x86_64-linux-gnu/libgmp.so.10
COPY --from=build /lib/x86_64-linux-gnu/libidn2.so.0 /lib/x86_64-linux-gnu/libidn2.so.0
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.3 /lib/x86_64-linux-gnu/libkrb5.so.3
COPY --from=build /lib/x86_64-linux-gnu/librtmp.so.1 /lib/x86_64-linux-gnu/librtmp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libuuid.so.1 /lib/x86_64-linux-gnu/libuuid.so.1
COPY --from=build /lib/x86_64-linux-gnu/libwind.so.0 /lib/x86_64-linux-gnu/libwind.so.0
COPY --from=build /lib/x86_64-linux-gnu/libcrypt.so.1 /lib/x86_64-linux-gnu/libcrypt.so.1
COPY --from=build /lib/x86_64-linux-gnu/libexpat.so.1 /lib/x86_64-linux-gnu/libexpat.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libhx509.so.5 /lib/x86_64-linux-gnu/libhx509.so.5
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.26 /lib/x86_64-linux-gnu/libkrb5.so.26
COPY --from=build /lib/x86_64-linux-gnu/libsasl2.so.2 /lib/x86_64-linux-gnu/libsasl2.so.2
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.1.1 /lib/x86_64-linux-gnu/libssl.so.1.1
COPY --from=build /lib/x86_64-linux-gnu/libtasn1.so.6 /lib/x86_64-linux-gnu/libtasn1.so.6
COPY --from=build /lib/x86_64-linux-gnu/libgssapi.so.3 /lib/x86_64-linux-gnu/libgssapi.so.3
COPY --from=build /lib/x86_64-linux-gnu/libnettle.so.7 /lib/x86_64-linux-gnu/libnettle.so.7
COPY --from=build /lib/x86_64-linux-gnu/libresolv.so.2 /lib/x86_64-linux-gnu/libresolv.so.2
COPY --from=build /lib/x86_64-linux-gnu/libroken.so.18 /lib/x86_64-linux-gnu/libroken.so.18
COPY --from=build /lib/x86_64-linux-gnu/libstdc++.so.6 /lib/x86_64-linux-gnu/libstdc++.so.6
COPY --from=build /lib/x86_64-linux-gnu/libcom_err.so.2 /lib/x86_64-linux-gnu/libcom_err.so.2
COPY --from=build /lib/x86_64-linux-gnu/libgnutls.so.30 /lib/x86_64-linux-gnu/libgnutls.so.30
COPY --from=build /lib/x86_64-linux-gnu/libhcrypto.so.4 /lib/x86_64-linux-gnu/libhcrypto.so.4
COPY --from=build /lib/x86_64-linux-gnu/libhogweed.so.5 /lib/x86_64-linux-gnu/libhogweed.so.5
COPY --from=build /lib/x86_64-linux-gnu/libp11-kit.so.0 /lib/x86_64-linux-gnu/libp11-kit.so.0
COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
COPY --from=build /lib/x86_64-linux-gnu/libsqlite3.so.0 /lib/x86_64-linux-gnu/libsqlite3.so.0
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.1.1 /lib/x86_64-linux-gnu/libcrypto.so.1.1
COPY --from=build /lib/x86_64-linux-gnu/libheimbase.so.1 /lib/x86_64-linux-gnu/libheimbase.so.1
COPY --from=build /lib/x86_64-linux-gnu/libheimntlm.so.0 /lib/x86_64-linux-gnu/libheimntlm.so.0
COPY --from=build /lib/x86_64-linux-gnu/libk5crypto.so.3 /lib/x86_64-linux-gnu/libk5crypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libkeyutils.so.1 /lib/x86_64-linux-gnu/libkeyutils.so.1
COPY --from=build /lib/x86_64-linux-gnu/liblber-2.4.so.2 /lib/x86_64-linux-gnu/liblber-2.4.so.2
COPY --from=build /lib/x86_64-linux-gnu/libnghttp2.so.14 /lib/x86_64-linux-gnu/libnghttp2.so.14
COPY --from=build /lib/x86_64-linux-gnu/libbrotlidec.so.1 /lib/x86_64-linux-gnu/libbrotlidec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libunistring.so.2 /lib/x86_64-linux-gnu/libunistring.so.2
COPY --from=build /lib/x86_64-linux-gnu/libldap_r-2.4.so.2 /lib/x86_64-linux-gnu/libldap_r-2.4.so.2
COPY --from=build /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /lib/x86_64-linux-gnu/libgssapi_krb5.so.2
COPY --from=build /lib/x86_64-linux-gnu/libkrb5support.so.0 /lib/x86_64-linux-gnu/libkrb5support.so.0
COPY --from=build /lib/x86_64-linux-gnu/libbrotlicommon.so.1 /lib/x86_64-linux-gnu/libbrotlicommon.so.1
COPY --from=build /opt/delft3dfm/lib/libwaq_plugin_wasteload.so.0 /opt/delft3dfm/lib/libwaq_plugin_wasteload.so.0
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//lib/libmpicxx.so.12 /opt/intel/oneapi/mpi/2021.6.0//lib/libmpicxx.so.12
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//lib/libmpifort.so.12 /opt/intel/oneapi/mpi/2021.6.0//lib/libmpifort.so.12
COPY --from=build /opt/intel/oneapi/mpi/2021.6.0//lib/release/libmpi.so.12 /opt/intel/oneapi/mpi/2021.6.0//lib/release/libmpi.so.12
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libimf.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libimf.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirc.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirc.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirng.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libirng.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libsvml.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libsvml.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libiomp5.so /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libiomp5.so
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libintlc.so.5 /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libintlc.so.5
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifport.so.5 /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifport.so.5
COPY --from=build /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifcoremt.so.5 /opt/intel/oneapi/compiler/2022.1.0/linux/compiler/lib/intel64_lin/libifcoremt.so.5


COPY --from=test_env /home /home