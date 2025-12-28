FROM inductiva/kutu:base-image_v0.1.1 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/fvcom-input-example.zip -P /home/ && \
    unzip /home/fvcom-input-example.zip -d /home/ && \
    rm /home/fvcom-input-example.zip

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/fvcom-input-example-wet-dry.zip -P /home/ && \
    unzip /home/fvcom-input-example-wet-dry.zip -d /home/ && \
    rm /home/fvcom-input-example-wet-dry.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1 as build

ENV PETSC_DIR=/petsc
ENV PETSC_ARCH=arch-linux-c-debug
ENV INCLUDEPATH=/usr/lib/x86_64-linux-gnu/fortran/gfortran-mod-15/openmpi:/FVCOM/src/libs/install/include/:/usr/include/

COPY make.inc /make.inc
COPY makefile /makefile
COPY make_estuary.inc /make_estuary.inc

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
    make && \
    mv fvcom /bin/fvcom && \
    mv make.inc /make.inc && \
    # compile another fvcom binary with nother flags
    mv -f /make_estuary.inc /FVCOM/src/make.inc && \
    make clean && \
    make && \
    mv fvcom /bin/fvcom_estuary && \
    mv make.inc /make_estuary.inc
    

COPY --from=test_env /home /home
