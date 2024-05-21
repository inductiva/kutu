# FROM inductiva/kutu:base-image_v0.1.0 as test_env

# RUN apt-get update && apt-get install -y \
#     wget \
#     unzip && \
#     wget https://storage.googleapis.com/inductiva-api-demo-files/openfast-input-example.zip -P /home/ && \
#     unzip /home/openfast-input-example.zip -d /home/ && \
#     rm /home/openfast-input-example.zip && \
#     ls -l

# COPY ./test_sim.sh /home/test_sim.sh
# RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.0 as build

RUN wget https://github.com/nwchemgit/nwchem/releases/download/v7.2.2-release/nwchem-7.2.2-release.revision-74936fb9-srconly.2023-11-03.tar.bz2 && \
    tar -xvjf nwchem-7.2.2-release.revision-74936fb9-srconly.2023-11-03.tar.bz2 && \
    export NWCHEM_TOP=/nwchem-7.2.2 && \
    export NWCHEM_TARGET=LINUX64 && \
    export ARMCI_NETWORK=MPI-MT && \
    export USE_MPI=y && \
    export USE_MPIF=y && \
    export NWCHEM_MODULES="all" && \
    #export USE_NOIO=TRUE
    export PYTHONVERSION=3.10 && \
    #You will also need to set PYTHONPATH to include any modules that you are
    #using in your input. Examples of Python within NWChem are in the
    #$NWCHEM_TOP/QA/tests/pyqa3 and $NWCHEM_TOP/contrib/python directories. 
    export BUILD_OPENBLAS=1 && \
    export BUILD_SCALAPACK=1 && \
    export BLAS_SIZE=4 && \
    export SCALAPACK_SIZE=4 && \
    cd $NWCHEM_TOP/src && \
    make nwchem_config && \
    make -j 4 && \
    #The script will choose the default memory settings based on the available
    #physical memory, recompile the appropriate files and relink.
    cd $NWCHEM_TOP/src && \
    ../contrib/getmem.nwchem
