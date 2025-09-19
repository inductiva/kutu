FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/cans-input-example.zip -P /home/ && \
    unzip /home/cans-input-example.zip -d /home/ && \
    rm /home/cans-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1 as build

RUN apt-get update && \
    apt-get install -y \
    libblas-dev \
	liblapack-dev \
	libparmetis-dev \
    libmumps-dev && \
    git clone --recursive https://github.com/ElmerCSC/elmerfem.git && \
    cd elmerfem && \
    git checkout afd75d44ce7a296321a2eb6d0c0a376fc326165c && \
    mkdir build && \
    cd build && \
    cmake .. \
		-DCMAKE_INSTALL_PREFIX=/usr/local/Elmer \
		-DCMAKE_C_COMPILER=/usr/bin/gcc \
		-DCMAKE_Fortran_COMPILER=/usr/bin/gfortran \
		-DWITH_MPI:BOOL=TRUE -DWITH_Mumps:BOOL=TRUE \
		-DWITH_Hypre:BOOL=FALSE -DWITH_Trilinos:BOOL=FALSE \
		-DWITH_ELMERGUI:BOOL=FALSE -DWITH_ElmerIce:BOOL=TRUE \
                -DWITH_LUA:BOOL=TRUE && \
    make && \
    make install && \
    cd / && \
    rm -r /elmerfem

# Set the path
ENV PATH=$PATH:/usr/local/Elmer/bin
ENV PATH=$PATH:/usr/local/Elmer/share/elmersolver/lib

ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1

COPY --from=test_env /home /home