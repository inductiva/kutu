#based on earlier work by Vladim Konjkov <Konjkov.VV@gmail.com>
#
# Create the image with the command
#  docker build -t nwchem-dev .
#
#after successful build one should run container to calculate input.nw file placed in <host_system_dir>
#docker run -dv <host_system_dir>:/data nwchem-dev "input.nw"
#this command return container ID to read logs by
#docker logs <container ID>
#

FROM        ubuntu:focal-20221130

LABEL maintainer="Edoardo Apra <edoardo.apra@pnnl.gov>"

LABEL org.opencontainers.image.description="NWChem image built from the master branch"
LABEL org.opencontainers.image.source "https://github.com/nwchemgit/nwchem"
LABEL org.opencontainers.image.documentation="https://nwchemgit.github.io/Containers.html"

#create user nwchem
RUN           groupadd -r nwchem -g 1994 \
              && useradd  -u 1994 -r -g nwchem -c 'NWChem user' -m -d /opt/nwchem -s /bin/bash nwchem 

#caching from host cache dir
COPY Dockerfile cache* /tmp/

ARG DEBIAN_FRONTEND=noninteractive
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ARG         FC
ARG         NWCHEM_BRANCH
ARG         GITHUB_REPOSITORY_OWNER
ARG CACHE_HIT
ENV         NWCHEM_TOP="/opt/nwchem"
ENV         FC=${FC}
ENV         NWCHEM_BRANCH=${NWCHEM_BRANCH}
ENV         GITHUB_REPOSITORY_OWNER=${GITHUB_REPOSITORY_OWNER}
ARG         NWCHEM_MODULES="all python "  \
            ARMCI_NETWORK=MPI-PT  \
            USE_OPENMP=1  \
            USE_NOIO=y  \
            USE_MPI=y  \
            USE_MPIF=y  \
            USE_MPIF4=y  \
	    BUILD_OPENBLAS=1 \
	    BUILD_SCALAPACK=1 \
	    BLAS_SIZE=8 \
	    SCALAPACK_SIZE=8 \
	    USE_HWOPT=n 
ENV         FFIELD=amber  \
            AMBER_1=${NWCHEM_TOP}/src/data/amber_s/  \
            AMBER_2=${NWCHEM_TOP}/src/data/amber_q/  \
            AMBER_3=${NWCHEM_TOP}/src/data/amber_x/  \
            AMBER_4=${NWCHEM_TOP}/src/data/amber_u/  \
            SPCE=${NWCHEM_TOP}/src/data/solvents/spce.rst  \
            CHARMM_S=${NWCHEM_TOP}/src/data/charmm_s/  \
            CHARMM_X=${NWCHEM_TOP}/src/data/charmm_x/  \
	    OMPI_MCA_btl_vader_single_copy_mechanism=none \
	    OMP_NUM_THREADS=1 \
	    COMEX_MAX_NB_OUTSTANDING=16 \
            PATH=${PATH}:/opt/nwchem/bin/LINUX64
WORKDIR	    /opt
#get NWCHEM_TARGET
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN ls -lrta /tmp && \
arch=$(uname -m) ; if [[ "$arch" == "x86_64" ]] || [[ "$arch" == "aarch64" ]] || [[ "$arch" == "riscv64" ]] || [[ "$arch" == "ppc64le" ]]; then echo "export NWCHEM_TARGET=LINUX64" > /tmpfile ; fi && \
arch_123=$(uname -m|cut -c 1-3); if [[ "$arch" == "i686" ]] || [[ "$arch" == "i386" ]] || [[ "$arch_123" == "arm" ]] ; then echo "export NWCHEM_TARGET=LINUX" > /tmpfile ; fi  &&\
. /tmpfile; echo "NWCHEM_TARGET is " ${NWCHEM_TARGET}  && \
     echo " defining modules according to CACHE_HIT= $CACHE_HIT and arch=$arch" && \
            if [[ ${FC} != "nvfortran" ]]; then export NWCHEM_MODULES+=" xtb "; fi &&\
	 if [[ "$arch" != "x86_64" ]]; then if  [[ "$CACHE_HIT" == "N" ]]; then export NWCHEM_MODULES="nwdft"; echo 'smaller build without cache. CACHE_HIT='$CACHE_HIT ; else echo 'large build with cache. CACHE_HIT='$CACHE_HIT ; export NWCHEM_MODULES="nwdft driver vib solvation gwmol python tce"  ; fi ;  fi &&\
	 if [[ $(echo $NWCHEM_MODULES |grep xtb) ]] ;then export USE_TBLITE=1; fi &&\
	     echo "  NWCHEM_MODULES= $NWCHEM_MODULES " && \
#one single ugly command to reduce docker size
            tries=0 ; until [ "$tries" -ge 10 ] ; do \
         apt-get -q=2 update \
            && apt-get -q=2 -y upgrade \
            && apt-get -q=2 install -y --no-install-recommends rsync python3-dev g++ gfortran libopenmpi-dev openmpi-bin  make unzip cmake git file wget curl tar bzip2 bc ca-certificates patch pkg-config libssl-dev python-is-python3 \
	    && break; \
	    tries=$((tries+1)) ; echo attempt no.  $tries    ; sleep 30 ;  done \
	    && export PYTHONVERSION=$(python -V| cut -d ' ' -f 2 |cut -d . -f 1-2) \
	    && echo FCFCFC is ${FC} \
	    && echo NWCHEM_BRANCH is ${NWCHEM_BRANCH} \
	    && echo GITHUB_REPOSITORY_OWNER is ${GITHUB_REPOSITORY_OWNER} \
	    && arch=$(uname -m) \
	    && echo arch is "$arch" \
	    && arch_dpkg=$(dpkg --print-architecture)  \
	    && if [[ "$arch" == "aarch64" ]]; then arch_dpkg="arm64"; fi \
	    && if [[ "$arch" == "x86_64" ]]; then arch_dpkg="amd64"; fi \
	    && nv_year=2022 && nv_major=22 &&  nv_minor=9 &&   nverdot="$nv_major"."$nv_minor" && nverdash="$nv_major"-"$nv_minor" \
	    &&  if [[ "$FC" == "nvfortran" ]]; then apt-get install -q=2 -y --no-install-recommends libtinfo5  libncursesw5 mpich libmpich-dev; wget --progress=dot:giga https://developer.download.nvidia.com/hpc-sdk/ubuntu/"$arch_dpkg/"nvhpc-"$nverdash"_"$nverdot"_$arch_dpkg.deb >& log1 ; wget --progress=dot:giga  https://developer.download.nvidia.com/hpc-sdk/ubuntu/$arch_dpkg/nvhpc-"$nv_year"_"$nverdot"_"$arch_dpkg".deb >&  log2 ; tail -n 2 log1 log2; ls -lrt nv*deb;  dpkg -i nvhpc*deb ; 	 /opt/nvidia/hpc_sdk/Linux_"$arch"/"$nverdot"/compilers/bin/makelocalrc -x ; export MPICH_FC="$FC" ; MPIF90=mpif90.mpich ; MPIRUN_PATH=/usr/bin/mpirun.mpich ; update-alternatives --set mpi /usr/bin/mpicc.mpich; update-alternatives --set mpirun  /usr/bin/mpirun.mpich; update-alternatives --list mpi  ; mpif90 -show; export ARMCI_NETWORK=MPI-TS;  rm -f nvhpc*deb ; mkdir -p /opt/lib || true; rsync -av /opt/nvidia/hpc_sdk/Linux_"$arch"/"$nverdot"/compilers/lib/*.so* /opt/lib/.; unset SCALAPACK_SIZE; unset BUILD_SCALAPACK; fi \
            &&  export PATH=/opt/nvidia/hpc_sdk/Linux_"$arch"/"$nverdot"/compilers/bin:"$PATH" \
            &&  export LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_"$arch"/"$nverdot"/compilers/lib:"$LD_LIBRARY_PATH" \
	    && echo "URL for cloning"  https://github.com/${GITHUB_REPOSITORY_OWNER}/nwchem.git \
	    && echo ca_certificate=/etc/ssl/certs/ca-certificates.crt >  ~/.wgetrc \
            && rm -rf nwchem||true; wget --progress=dot:giga https://github.com/${GITHUB_REPOSITORY_OWNER}/nwchem/tarball/"$NWCHEM_BRANCH" -O - | tar -xz  --exclude=web --exclude=examples --exclude=doc --exclude="nwxc*"  --exclude="chem-library-tests" \
	    &&    mv ${GITHUB_REPOSITORY_OWNER}-nwchem-* nwchem \
            && cd nwchem/src \
#set NWCHEM_TARGET 
            &&  . /tmpfile; echo "NWCHEM_TARGET is " ${NWCHEM_TARGET} \
	    && echo "NWCHEM_MODULES is " ${NWCHEM_MODULES} \
#fix openblas cross-compilation
            && arch=$(uname -m) \
            && arch3=$(uname -m|cut -c 1-3) \
            && arch5=$(uname -m|cut -c 1-5) \
	    &&  if [[ "$FC" == "nvfortran" ]] && [[ "$arch" == "aarch64" ]]; then  cd /tmp ; wget --progress=dot:giga https://raw.githubusercontent.com/${GITHUB_REPOSITORY_OWNER}/nwchem-dockerfiles/master/patches/nv_arm64.patch; cd / ; patch -p0 < /tmp/nv_arm64.patch; cd /opt/nwchem/src; fi \
	    && if [[ "$arch" == "aarch64" ]]; then export FORCETARGET=" TARGET=ARMV8 "; fi \
	    && if [[ "$arch" == "ppc64le" ]]; then export FORCETARGET=" TARGET=POWER8 "; fi \
	    && if [[ "$arch" == "riscv64" ]]; then export FORCETARGET=" TARGET=RISCV64_GENERIC "; export ARMCI_NETWORK=MPI-TS; unset USE_OPENMP; fi \
	    && if [[ "$arch5" == "armv6" ]]; then export FORCETARGET=" TARGET=ARMV6 "; fi \
	    && if [[ "$arch5" == "armv7" ]]; then export FORCETARGET=" TARGET=ARMV7 "; export ARMCI_NETWORK=MPI-TS; fi \
# _SIZE=4 and openblas pkg for 32bit archs
	    && if [[ ${NWCHEM_TARGET} == "LINUX" ]]; then export BLAS_SIZE=4; unset SCALAPACK_SIZE; unset BUILD_SCALAPACK; unset  BUILD_OPENBLAS; export BLASOPT=-lopenblas ; export LAPACK_LIB=-lopenblas;  apt-get -q=2 install -y --no-install-recommends openmpi-bin libopenblas-dev; fi  \
# smaller build on qemu emulated archs
	    && if [[ "$arch" != "x86_64" ]]; then export NWCHEM_MODULES="nwdft driver solvation python"; fi \
# compile libxc for amd64 
	    && if [[ "$arch" == "x86_64" ]]; then export USE_LIBXC=1;  \
	    export USE_SIMINT=1; export SIMINT_MAXAM=5; export SIMINT_VECTOR=avx2 ; fi \
            && if [[ -f /tmp/libext.tar.bz2 ]]; then cd libext ; tar xjvf /tmp/libext.tar.bz2; rm -rf /tmp/libext.tar.bz2 ; cd ..  ; fi \
            && if [[ -f /tmp/simint.tar.bz2 ]]; then cd NWints/simint/libsimint_source ; tar xjf /tmp/simint.tar.bz2; rm -rf /tmp/simint.tar.bz2 ; cd ../../..  ; fi\
	    && df -h /dev/shm \
            && mkdir -p ../bin/${NWCHEM_TARGET} \
            && gcc -o ../bin/"$NWCHEM_TARGET/depend.x" config/depend.c \
            && make nwchem_config \
            && cd libext   && make V=-1  && cd .. \
            && cd tools    && make V=-1  && cd .. \
            && ( make USE_INTERNALBLAS=y deps_stamp  >& deps.log &) \
	    && sleep 15s \
	    && echo tail deps.log '@@@' \
	    && tail -10  deps.log \
	    && echo done tail deps.log '@@@' \
            && if [[ "$arch" != "x86_64" ]] && [[ "$CACHE_HIT" == "N" ]]; then make FOPTIMIZE=-O1 FDEBUG=-O0\ -g ; else  make  V=-1 ; fi ||true\
	    &&  if [[ -f ../bin/${NWCHEM_TARGET}/nwchem ]]; then echo 'NWChem binary created' ; else  echo 'compilation error1'; exit 1; fi \
            &&     ../contrib/getmem.nwchem 1000  || true \
	    &&  if [[ -f ../bin/${NWCHEM_TARGET}/nwchem ]]; then echo 'NWChem binary created' ; else  echo 'compilation error2'; exit 1; fi \
# QA tests
            && cd .. \
            && if [[ ${NWCHEM_TARGET} == "LINUX64" && "$FC" != "nvfortran" ]]; then SKIP_CACHE=1 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \
	    NWCHEM_EXECUTABLE=$(pwd)/bin/${NWCHEM_TARGET}/nwchem ./travis/run_qas.sh ; fi \
	    && cd src \
#clean unnecessary source to reduce docker size
            && rm -rf tce tools nwdft geom symmetry util nwxc ddscf lapack blas rism argos peigs rmdft gradients symmetry property smd lucia dplot propery hessian ccsd mp2_grad moints cafe analyz dimqm /opt/nwchem/lib libext/scalapack libext/openblas  develop ../QA ../contrib ../examples ../.git ../travis ../web nwpw/nwpwlib/nwpwxc rdmft ../doc libext/libxc/libxc* libext/mpich  /tmp/libext || true \
	    && ls -lrt libext/libxc || true \
	    && ls -lrt libext/lib || true \
	    && strip ../bin/${NWCHEM_TARGET}/nwchem \
	    && rm libext/libxc/install/bin/xc* || true \
	    && cd libext ; tar cjvf libext.tar.bz2 include/* lib/* libxc/install/lib/* libxc/install/include/* ||true \
	    && rm -rf lib/* libxc/install/lib/* ||true \
	    && cd $NWCHEM_TOP/src/NWints/simint/libsimint_source/ ; tar cjvf $NWCHEM_TOP/src/libext/simint.tar.bz2 simint_install/* || true \
	    && cd  $NWCHEM_TOP/src &&  rm -rf NWints || true \
	    && cd $NWCHEM_TOP/src || { echo "Failure"; exit 1; } \
	    && cd $NWCHEM_TOP \
#clean unnecessary packages
            && DEBIAN_FRONTEND=noninteractive apt-get -q=2 -y install --no-install-recommends localepurge \
	    && echo MANDELETE >  /etc/locale.nopurge \
	    && echo DONTBOTHERNEWLOCALE >> /etc/locale.nopurge \
	    && echo en_US.UTF-8 >> /etc/locale.nopurge \
	    && localepurge \
	    && rm -rf /usr/share/doc \
            &&       apt-get -q=2 -y purge  wget curl git make unzip cmake cmake-data libhwloc-plugins libicu66 manpages manpages-dev iproute2 libelf1 libmnl0 libxtables12 libxau6 libxcb1 libxdmcp6 libx11-6 libx11-data libxext6 libxmuu1 xauth xz-utils localepurge  g++-8 g++ libstdc++-9-dev libopenmpi-dev perl libhwloc-dev libibverbs-dev libopenmpi-dev libcoarrays-dev libcoarrays-openmpi-dev libevent-dev libltdl-dev libnl-3-dev libnl-route-3-dev libnuma-dev autoconf automake autotools-dev libcaf-openmpi-3 libevent-extra-2.1-7 libsigsegv2 libtool ibverbs-providers bc &&  apt-get -y autoremove && apt-get -q=2 -y install libopenmpi3 && apt-get clean \
           && apt-get -y purge cpp-9 gfortran-9 gcc-9  libnl-3-dev libnl-route-3-dev libnuma-dev libibverbs-dev libgcc-9-dev autotools-dev libevent-dev libpython3.8-dev libc6-dev linux-libc-dev libexpat1-dev zlib1g-dev libcrypt-dev perl-modules-5.30 libperl5.30  || true \
	   && apt-get clean \
           && if [[ ${NWCHEM_TARGET} == "LINUX" ]]; then apt-get -y purge libopenblas-dev; fi \
           && if [[ "$FC" == "nvfortran" ]]; then rm -f /opt/lib/*lp64* /opt/lib/*cudafor* ;fi \
	   && rm -rf /opt/nwchem/src/libext/libext_utils || true \
	   && chown -R nwchem /opt/nwchem && chgrp -R nwchem /opt/nwchem \
	   && du -sh /opt/nwchem \
	   && du -sh /opt/nwchem/src/libext/lib || true \
	   && du -sk /opt/nwchem/*|sort -n \
	   && ls -lrt /opt/lib || true \
	   && du -sh /opt/nvidia || true \
	   && dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n | tail -n 100
	   
ENV LD_LIBRARY_PATH /opt/lib


USER        nwchem

WORKDIR     /data
ENTRYPOINT  ["nwchem"]

##CMD ["/bin/bash"]