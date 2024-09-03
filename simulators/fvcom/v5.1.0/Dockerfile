# FROM inductiva/kutu:base-image_v0.1.1 as test_env

# RUN wget https://storage.googleapis.com/inductiva-api-demo-files/cans-input-example.zip -P /home/ && \
#     unzip /home/cans-input-example.zip -d /home/ && \
#     rm /home/cans-input-example.zip

# COPY ./test_sim.sh /home/test_sim.sh
# RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1 as build

# ---------- from 4.4.7 ----------

# ------- Petsc -------
# download petsc git clone -b release https://gitlab.com/petsc/petsc.git petsc
# export PETSC_DIR=/petsc
# export PETSC_ARCH=arch-linux-c-debug
# cd $PETSC_DIR
# ./configure --download-hypre --with-hypre
# make PETSC_DIR=/petsc PETSC_ARCH=arch-linux-c-debug all

# cd /FVCOM/src
# edit makefile.inc
# define TOPDIR = /FVCOM/src
# comment/uncomment petsc version 3.18
# Comment intel compiler definitions
# uncomment gfortran defs
# add this flags to the gfortran defs
# Move -O3 from FC to DEBFLGS = -O3
# OPT      = -ffixed-line-length-none -ffree-line-length-0 -fallow-argument-mismatch
#This is the result
#  gfortran defs
#--------------------------------------------------------------------------
#  CPP      = /usr/bin/cpp
#  COMPILER = -DGFORTRAN
#  FC       = gfortran
#  DEBFLGS  = -O3
#  OPT      = -ffixed-line-length-none -ffree-line-length-0 -fallow-argument-mismatch
#  CLIB     =
# ----more edits----
# comment If FLAG_411 is defined, uncomment path below the lines below
# uncomment 
#        If FLAG_411 is not defined, uncomment path below
#             PARLIB = -L/usr/lib/x86_64-linux-gnu/ -lmetis
#             PARTINCS =
#             PARTLIBS =
# change julian link to
# -L/FVCOM/src/libs/install/lib

#Edit the files 
# mod_station_timeseries.f90
#old->WRITE(10,'(2I10,<MX_NBR_ELEM_GL+1>I10)') I,NTVEGL(I),(NBVEGL(I,J),J=1,NTVEGL(I))
#new->WRITE(10,'(2I10,"<MX_NBR_ELEM_GL+1>"I10)') I,NTVEGL(I),(NBVEGL(I,J),J=1,NTVEGL(I))

#mod_action_ex.F
#old->    EXFLUXA=-UNA*((1.0+SIGN(REAL(1.0,SP),UNA))*FIJ2A(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),UNA))*FIJ1A(:,:,IA))*0.5
#old->    EXFLUXB=-UNBB*((1.0+SIGN(REAL(1.0,SP),UNBB))*FIJ2B(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),UNBB))*FIJ1B(:,:,IA))*0.5
#new->    EXFLUXA=-UNA*((1.0+SIGN(REAL(1.0,SP),REAL(UNA,SP)))*FIJ2A(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),REAL(UNA,SP)))*FIJ1A(:,:,IA))*0.5
#new->    EXFLUXB=-UNBB*((1.0+SIGN(REAL(1.0,SP),REAL(UNBB,SP)))*FIJ2B(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),REAL(UNBB,SP)))*FIJ1B(:,:,IA))*0.5

#ocpcre.F
#old->     IF(ELTYPE == 'KEY' .AND. KEYWIS==.TRUE.) ELTYPE = 'USED'
#new->     IF((ELTYPE == 'KEY') .AND. (KEYWIS .EQV. .TRUE.)) ELTYPE = 'USED'

# cd /FVCOM/src/libs
# edit makefile
# uncomment the PACKAGES to have all libs
# we have netcdf installed from apt-get
# comment cd netcdf && make install
# replace 
#cd fproj && ./configure CPPFLAGS='$(COMPILER)' CC=$(CC) CFLAGS=-O3
#with
#cd fproj && ./configure CPPFLAGS='$(COMPILER)' CC=$(CC) CFLAGS="-O3 -Df2cFortran"

#cd /FVCOM/src/
#export INCLUDEPATH=/usr/lib/x86_64-linux-gnu/fortran/gfortran-mod-15/openmpi
#export INCLUDEPATH="$INCLUDEPATH:/FVCOM/src/libs/install/include"
#export INCLUDEPATH="$INCLUDEPATH:/usr/include/"
#metis from libs is broken https://www.math-linux.com/mathematics/linear-systems/article/how-to-patch-metis-4-0-error-conflicting-types-for-__log2
#install from apt-get install libmetis-dev
# make -j

ENV PETSC_DIR=/petsc
ENV PETSC_ARCH=arch-linux-c-debug
ENV INCLUDEPATH=/usr/lib/x86_64-linux-gnu/fortran/gfortran-mod-15/openmpi:/FVCOM/src/libs/install/include/:/usr/include/

COPY make.inc /make.inc
COPY makefile /makefile

RUN apt-get install libmetis-dev -y && \
    git clone --branch v5.1.0 https://github.com/FVCOM-GitHub/FVCOM.git && \
    cd FVCOM && \
    cd / && \
    mv -f /make.inc /FVCOM/src/make.inc && \
    mv -f /makefile /FVCOM/src/libs/makefile && \
    git clone -b release https://gitlab.com/petsc/petsc.git petsc && \
    cd $PETSC_DIR && \
    ./configure --download-hypre --with-hypre && \
    make PETSC_DIR=/petsc PETSC_ARCH=arch-linux-c-debug all && \
    cd /FVCOM/src && \
    sed -i "s/WRITE(10,'(2I10,<MX_NBR_ELEM_GL+1>I10)')/WRITE(10,'(2I10,\"<MX_NBR_ELEM_GL+1>\"I10)')/g" mod_station_timeseries.F && \
    sed -i "s/EXFLUXA=-UNA*((1.0+SIGN(REAL(1.0,SP),UNA))*FIJ2A(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),UNA))*FIJ1A(:,:,IA))*0.5/EXFLUXA=-UNA*((1.0+SIGN(REAL(1.0,SP),REAL(UNA,SP)))*FIJ2A(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),REAL(UNA,SP)))*FIJ1A(:,:,IA))*0.5/g" mod_action_ex.F && \
    sed -i "s/EXFLUXB=-UNBB*((1.0+SIGN(REAL(1.0,SP),UNBB))*FIJ2B(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),UNBB))*FIJ1B(:,:,IA))*0.5/EXFLUXB=-UNBB*((1.0+SIGN(REAL(1.0,SP),REAL(UNBB,SP)))*FIJ2B(:,:,IB)+(1.0-SIGN(REAL(1.0,SP),REAL(UNBB,SP)))*FIJ1B(:,:,IA))*0.5/g" mod_action_ex.F && \
    sed -i "s/IF(ELTYPE == 'KEY' .AND. KEYWIS==.TRUE.) ELTYPE = 'USED'/IF((ELTYPE == 'KEY') .AND. (KEYWIS .EQV. .TRUE.)) ELTYPE = 'USED'/g" ocpcre.F && \
    cd /FVCOM/src/libs && \
    make && \
    cd /FVCOM/src && \
    make
    
FROM ubuntu:22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean

COPY --from=build /FVCOM/src/fvcom /fvcom
COPY ./test_sim.sh /home/test_sim.sh

COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
COPY --from=build /lib/x86_64-linux-gnu/libz.so.1 /lib/x86_64-linux-gnu/libz.so.1
COPY --from=build /lib/x86_64-linux-gnu/libsz.so.2 /lib/x86_64-linux-gnu/libsz.so.2
COPY --from=build /lib/x86_64-linux-gnu/libssh.so.4 /lib/x86_64-linux-gnu/libssh.so.4
COPY --from=build /lib/x86_64-linux-gnu/libpsl.so.5 /lib/x86_64-linux-gnu/libpsl.so.5
COPY --from=build /lib/x86_64-linux-gnu/libssl.so.3 /lib/x86_64-linux-gnu/libssl.so.3
COPY --from=build /lib/x86_64-linux-gnu/libaec.so.0 /lib/x86_64-linux-gnu/libaec.so.0
COPY --from=build /lib/x86_64-linux-gnu/libffi.so.8 /lib/x86_64-linux-gnu/libffi.so.8
COPY --from=build /lib/x86_64-linux-gnu/libmvec.so.1 /lib/x86_64-linux-gnu/libmvec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libmpi.so.40 /lib/x86_64-linux-gnu/libmpi.so.40
COPY --from=build /lib/x86_64-linux-gnu/libcurl.so.4 /lib/x86_64-linux-gnu/libcurl.so.4
COPY --from=build /lib/x86_64-linux-gnu/libidn2.so.0 /lib/x86_64-linux-gnu/libidn2.so.0
COPY --from=build /lib/x86_64-linux-gnu/librtmp.so.1 /lib/x86_64-linux-gnu/librtmp.so.1
COPY --from=build /lib/x86_64-linux-gnu/libzstd.so.1 /lib/x86_64-linux-gnu/libzstd.so.1
COPY --from=build /lib/x86_64-linux-gnu/libudev.so.1 /lib/x86_64-linux-gnu/libudev.so.1
COPY --from=build /lib/x86_64-linux-gnu/libgmp.so.10 /lib/x86_64-linux-gnu/libgmp.so.10
COPY --from=build /lib/x86_64-linux-gnu/libkrb5.so.3 /lib/x86_64-linux-gnu/libkrb5.so.3
COPY --from=build /lib/x86_64-linux-gnu/libmetis.so.5 /lib/x86_64-linux-gnu/libmetis.so.5
COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
COPY --from=build /lib/x86_64-linux-gnu/libsasl2.so.2 /lib/x86_64-linux-gnu/libsasl2.so.2
COPY --from=build /lib/x86_64-linux-gnu/libtasn1.so.6 /lib/x86_64-linux-gnu/libtasn1.so.6
COPY --from=build /lib/x86_64-linux-gnu/libhwloc.so.15 /lib/x86_64-linux-gnu/libhwloc.so.15
COPY --from=build /lib/x86_64-linux-gnu/libcrypto.so.3 /lib/x86_64-linux-gnu/libcrypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libnettle.so.8 /lib/x86_64-linux-gnu/libnettle.so.8
COPY --from=build /lib/x86_64-linux-gnu/libresolv.so.2 /lib/x86_64-linux-gnu/libresolv.so.2
COPY --from=build /lib/x86_64-linux-gnu/libnetcdff.so.7 /lib/x86_64-linux-gnu/libnetcdff.so.7
COPY --from=build /lib/x86_64-linux-gnu/libnetcdf.so.19 /lib/x86_64-linux-gnu/libnetcdf.so.19
COPY --from=build /lib/x86_64-linux-gnu/libgnutls.so.30 /lib/x86_64-linux-gnu/libgnutls.so.30
COPY --from=build /lib/x86_64-linux-gnu/libhogweed.so.6 /lib/x86_64-linux-gnu/libhogweed.so.6
COPY --from=build /lib/x86_64-linux-gnu/libcom_err.so.2 /lib/x86_64-linux-gnu/libcom_err.so.2
COPY --from=build /lib/x86_64-linux-gnu/libp11-kit.so.0 /lib/x86_64-linux-gnu/libp11-kit.so.0
COPY --from=build /lib/x86_64-linux-gnu/libgfortran.so.5 /lib/x86_64-linux-gnu/libgfortran.so.5
COPY --from=build /lib/x86_64-linux-gnu/libquadmath.so.0 /lib/x86_64-linux-gnu/libquadmath.so.0
COPY --from=build /lib/x86_64-linux-gnu/libnghttp2.so.14 /lib/x86_64-linux-gnu/libnghttp2.so.14
COPY --from=build /lib/x86_64-linux-gnu/libldap-2.5.so.0 /lib/x86_64-linux-gnu/libldap-2.5.so.0
COPY --from=build /lib/x86_64-linux-gnu/liblber-2.5.so.0 /lib/x86_64-linux-gnu/liblber-2.5.so.0
COPY --from=build /lib/x86_64-linux-gnu/libk5crypto.so.3 /lib/x86_64-linux-gnu/libk5crypto.so.3
COPY --from=build /lib/x86_64-linux-gnu/libkeyutils.so.1 /lib/x86_64-linux-gnu/libkeyutils.so.1
COPY --from=build /lib/x86_64-linux-gnu/libopen-pal.so.40 /lib/x86_64-linux-gnu/libopen-pal.so.40
COPY --from=build /lib/x86_64-linux-gnu/libopen-rte.so.40 /lib/x86_64-linux-gnu/libopen-rte.so.40
COPY --from=build /lib/x86_64-linux-gnu/libbrotlidec.so.1 /lib/x86_64-linux-gnu/libbrotlidec.so.1
COPY --from=build /lib/x86_64-linux-gnu/libunistring.so.2 /lib/x86_64-linux-gnu/libunistring.so.2
COPY --from=build /lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /lib/x86_64-linux-gnu/libmpi_mpifh.so.40
COPY --from=build /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /lib/x86_64-linux-gnu/libgssapi_krb5.so.2
COPY --from=build /lib/x86_64-linux-gnu/libkrb5support.so.0 /lib/x86_64-linux-gnu/libkrb5support.so.0
COPY --from=build /lib/x86_64-linux-gnu/libbrotlicommon.so.1 /lib/x86_64-linux-gnu/libbrotlicommon.so.1
COPY --from=build /lib/x86_64-linux-gnu/libhdf5_serial.so.103 /lib/x86_64-linux-gnu/libhdf5_serial.so.103
COPY --from=build /lib/x86_64-linux-gnu/libevent_core-2.1.so.7 /lib/x86_64-linux-gnu/libevent_core-2.1.so.7
COPY --from=build /lib/x86_64-linux-gnu/libhdf5_serial_hl.so.100 /lib/x86_64-linux-gnu/libhdf5_serial_hl.so.100
COPY --from=build /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7 /lib/x86_64-linux-gnu/libevent_pthreads-2.1.so.7