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

ENV NWCHEM_TOP=/nwchem-7.2.2 \
	NWCHEM_TARGET=LINUX64 \
	ARMCI_NETWORK=MPI-MT \
	#lets try to build with no mpi
	# we were having problems with the mpi maybe something with fortan and mpi
	# USE_MPI=y \
	# USE_MPIF=y \
	NWCHEM_MODULES="all" \
	PYTHONVERSION=3.10 \
	#using or compiling openblas and lapak was giving erros TODO later
	USE_INTERNALBLAS=y

RUN wget https://github.com/nwchemgit/nwchem/releases/download/v7.2.2-release/nwchem-7.2.2-release.revision-74936fb9-srconly.2023-11-03.tar.bz2 && \
    tar -xvjf nwchem-7.2.2-release.revision-74936fb9-srconly.2023-11-03.tar.bz2 && \
    #export USE_NOIO=TRUE
    #You will also need to set PYTHONPATH to include any modules that you are
    #using in your input. Examples of Python within NWChem are in the
    #$NWCHEM_TOP/QA/tests/pyqa3 and $NWCHEM_TOP/contrib/python directories. 
    # export BUILD_OPENBLAS=1 && \
    # export BUILD_SCALAPACK=1 && \
    # export BLAS_SIZE=4 && \
    # export SCALAPACK_SIZE=4 && \
    cd $NWCHEM_TOP/src

			# Do this inside the docker to try to fix the error
			# Warning: Rank mismatch between actual argument at (1) and actual argument at (2) (scalar and rank-1)
			# Compiling rohf_dens.F...
			# Compiling movecs_phase.F...
			# Compiling riscf_fock.F...
			# Compiling riscf_init.F...
			# f951: Warning: Nonexistent include directory '-I/nwchem-7.2.2/src/include' [-Wmissing-include-dirs]
			# riscf_init.F:16:2:
			# riscf_init.F:16:2:

			# 16 |
			# 	|  1
			# Fatal Error: errquit.fh: No such file or directory
			# compilation terminated.
			# make[1]: *** [../config/makefile.h:4032: /nwchem-7.2.2/lib/LINUX64/libddscf.a(riscf_init.o)] Error 1
			# make[1]: Leaving directory '/nwchem-7.2.2/src/ddscf'
			# make: *** [GNUmakefile:105: libraries] Error 1
			# https://verahill.blogspot.com/2013/02/340-issues-when-compiling-nwchem-611.html


			#see this if we have more problems
			# https://verahill.blogspot.com/2017/09/646-nwchem-66-on-debian-stretch-9.html

    # make nwchem_config && \
    # make -j 4 && \
    # #The script will choose the default memory settings based on the available
    # #physical memory, recompile the appropriate files and relink.
    # cd $NWCHEM_TOP/src && \
    # ../contrib/getmem.nwchem