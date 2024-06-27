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

FROM ubuntu:22.04

RUN apt update -qq && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean
COPY --from=build /nwchem-7.2.2/bin/LINUX64/nwchem /bin/nwchem
COPY --from=test_env /home /home
