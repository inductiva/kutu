FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/nwchem-input-example.zip -P /home/ && \
    unzip /home/nwchem-input-example.zip -d /home/ && \
    rm /home/nwchem-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.0 as build

ENV NWCHEM_TOP=/nwchem-7.2.2 \
	NWCHEM_TARGET=LINUX64 \
	ARMCI_NETWORK=MPI-MT \
	NWCHEM_MODULES=all \
	PYTHONVERSION=3.10 \
	USE_OPENMP=1  \
	USE_NOIO=y  \
	USE_MPI=y \
	USE_MPIF=y \
	USE_MPIF4=y \
	LARGE_FILES=TRUE \
	#using or compiling openblas and lapak was giving erros TODO later
	USE_INTERNALBLAS=y

RUN wget https://github.com/nwchemgit/nwchem/releases/download/v7.2.2-release/nwchem-7.2.2-release.revision-74936fb9-srconly.2023-11-03.tar.bz2 && \
    tar -xvjf nwchem-7.2.2-release.revision-74936fb9-srconly.2023-11-03.tar.bz2 && \
    cd $NWCHEM_TOP/src && \
    make nwchem_config && \
    make V=1 USE_INTERNALBLAS=y
RUN cd $NWCHEM_TOP/src && \
    make clean

FROM ubuntu:22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean


COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /lib/x86_64-linux-gnu/libmpi_mpifh.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libgfortran.so.5 /lib/x86_64-linux-gnu/libgfortran.so.5
COPY --from=build /lib/x86_64-linux-gnu/libquadmath.so.0 /lib/x86_64-linux-gnu/libquadmath.so.0
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libmvec.so.1 /lib/x86_64-linux-gnu/libmvec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgomp.so.1 /lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2

COPY --from=build /nwchem-7.2.2/bin/LINUX64/nwchem /bin/nwchem
COPY --from=build /nwchem-7.2.2/src /nwchem-7.2.2/src
COPY --from=test_env /home /home
