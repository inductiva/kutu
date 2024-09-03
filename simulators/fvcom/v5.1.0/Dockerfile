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
    
#FROM ubuntu:22.04