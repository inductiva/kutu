FROM inductiva/kutu:base-image_v0.1.1_dev AS test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/openfoam-esi-input-example.zip -P /home/ && \
    unzip /home/openfoam-esi-input-example.zip -d /home/ && \
    rm /home/openfoam-esi-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1_dev AS build

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV FOAM_EXT_LIBBIN=/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/lib/

ARG openfoam_num_version=2406
ARG openfoam_version="openfoam${openfoam_num_version}"

RUN apt-get update && \
	apt install -y paraview-dev \
        cmake qtbase5-dev qttools5-dev \
        qttools5-dev-tools libqt5opengl5-dev \
        libqt5x11extras5-dev libxt-dev flex

RUN wget "https://altushost-swe.dl.sourceforge.net/project/openfoam/v2406/OpenFOAM-v2406.tgz?viasf=1" -O OpenFOAM-v2406.tgz && \
	tar -xzf OpenFOAM-v2406.tgz && \
	cd OpenFOAM-v${openfoam_num_version} && \
	source etc/bashrc && \
    wget "https://deac-fra.dl.sourceforge.net/project/openfoam/v2406/ThirdParty-v2406.tgz?viasf=1" -O ThirdParty-v2406.tgz && \
	tar -xzf ThirdParty-v2406.tgz && \
	mv ThirdParty-v2406 ThirdParty && \
    rm /OpenFOAM-v2406/ThirdParty-v2406.tgz && \
	./Allwmake -j

FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

ENV OPENFOAM_SOURCE_FILE=/OpenFOAM-v2406/etc/bashrc
ARG DEBIAN_FRONTEND=noninteractive

#run as root
RUN apt update -qq && \
    #https://develop.openfoam.com/Development/openfoam/blob/develop/doc/Requirements.md
	apt-get install -y make \
        gcc \
        g++ \
        autoconf \
        autotools-dev \
        cmake \
        gawk \
        gnuplot \
        flex \
        libfl-dev \
        libreadline-dev \
        zlib1g-dev \
        libgmp-dev \
        libmpfr-dev \
        libmpc-dev && \
    apt install --no-install-recommends -y \
        openmpi-bin=4.1.2-2ubuntu1 && \
    apt clean && \
    apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* && \
    # Create user openfoam_user
    useradd -ms /bin/bash openfoam_user
# Switch to user openfoam_user
USER openfoam_user

COPY --from=build --chown=openfoam_user /OpenFOAM-v2406 /OpenFOAM-v2406
COPY --from=test_env --chown=openfoam_user /home /home
COPY --chown=openfoam_user ./launch.sh /launch.sh
COPY ./functions/isParallel /bin/isParallel
COPY ./functions/isTest /bin/isTest
COPY ./functions/notTest /bin/notTest
COPY ./functions/canCompile /bin/canCompile
COPY ./functions/isTrue /bin/isTrue
COPY ./functions/getNumberOfPatchFaces /bin/getNumberOfPatchFaces
COPY ./functions/getNumberOfProcessors /bin/getNumberOfProcessors
COPY ./functions/getApplication /bin/getApplication
COPY ./functions/runApplication /bin/runApplication
COPY ./functions/runParallel /bin/runParallel
COPY ./functions/compileApplication /bin/compileApplication
COPY ./functions/cloneCase /bin/cloneCase
COPY ./functions/cloneParallelCase /bin/cloneParallelCase
COPY ./functions/restore0Dir /bin/restore0Dir

# run as openfoam_user
RUN chmod +x /launch.sh && \
	cd /OpenFOAM-v2406 && \
	source etc/bashrc && \
	# This second Allwmake is necessary
	# https://www.cfd-online.com/Forums/openfoam-installation/100347-libscotch-so-missing.html
	./Allwmake -j && \
    rm -r /OpenFOAM-v2406/ThirdParty/build/ && \
    rm -r /OpenFOAM-v2406/build/ && \
    rm -r /OpenFOAM-v2406/ThirdParty/sources/ && \
    #cant delete src folders because it might be needed to create new libraries
    #in some cases some libraries cannot be loaded so Openfoam creates them
    #on the fly (we need src for that)
    chmod +x /bin/isParallel && \
    chmod +x /bin/isTest && \
    chmod +x /bin/notTest && \
    chmod +x /bin/canCompile && \
    chmod +x /bin/isTrue && \
    chmod +x /bin/getNumberOfPatchFaces && \
    chmod +x /bin/getNumberOfProcessors && \
    chmod +x /bin/getApplication && \
    chmod +x /bin/runApplication && \
    chmod +x /bin/runParallel && \
    chmod +x /bin/compileApplication && \
    chmod +x /bin/cloneCase && \
    chmod +x /bin/cloneParallelCase && \
    chmod +x /bin/restore0Dir

ENV FOAM_API=2406
ENV WM_COMPILER=Gcc
ENV WM_ARCH=linux64
ENV WM_LABEL_SIZE=32
ENV MPI_ARCH_PATH=/usr
ENV WM_PROJECT=OpenFOAM
ENV FOAM_MPI=sys-openmpi
ENV WM_LABEL_OPTION=Int32
ENV WM_COMPILE_OPTION=Opt
ENV WM_PRECISION_OPTION=DP
ENV WM_MPLIB=SYSTEMOPENMPI
ENV WM_COMPILER_TYPE=system
ENV WM_COMPILER_LIB_ARCH=64
ENV WM_PROJECT_VERSION=v2406
ENV FOAM_ETC=/OpenFOAM-v2406/etc
ENV WM_DIR=/OpenFOAM-v2406/wmake
ENV FOAM_SRC=/OpenFOAM-v2406/src
ENV WM_PROJECT_DIR=/OpenFOAM-v2406
ENV WM_OPTIONS=linux64GccDPInt32Opt
ENV FOAM_APP=/OpenFOAM-v2406/applications
ENV FOAM_TUTORIALS=/OpenFOAM-v2406/tutorials
ENV WM_THIRD_PARTY_DIR=/OpenFOAM-v2406/ThirdParty
ENV FOAM_SOLVERS=/OpenFOAM-v2406/applications/solvers
ENV FOAM_RUN=/home/openfoam_user/OpenFOAM/user-v2406/run
ENV FOAM_UTILITIES=/OpenFOAM-v2406/applications/utilities
ENV WM_PROJECT_USER_DIR=/home/openfoam_user/OpenFOAM/user-v2406
ENV FOAM_APPBIN=/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/bin
ENV FOAM_LIBBIN=/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/lib
ENV CGAL_ARCH_PATH=/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/CGAL-4.14.3
ENV FOAM_EXT_LIBBIN=/OpenFOAM-v2406/ThirdParty/platforms/linux64GccDPInt32/lib
ENV FFTW_ARCH_PATH=/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/fftw-3.3.10
ENV BOOST_ARCH_PATH=/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/boost_1_74_0
ENV FOAM_SITE_LIBBIN=/OpenFOAM-v2406/site/2406/platforms/linux64GccDPInt32Opt/lib
ENV FOAM_SITE_APPBIN=/OpenFOAM-v2406/site/2406/platforms/linux64GccDPInt32Opt/bin
ENV ADIOS2_ARCH_PATH=/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/ADIOS2-2.10.1
ENV SCOTCH_ARCH_PATH=/OpenFOAM-v2406/ThirdParty/platforms/linux64GccDPInt32/scotch_6.1.0
ENV FOAM_USER_LIBBIN=/home/openfoam_user/OpenFOAM/user-v2406/platforms/linux64GccDPInt32Opt/lib
ENV FOAM_USER_APPBIN=/home/openfoam_user/OpenFOAM/user-v2406/platforms/linux64GccDPInt32Opt/bin
ENV PATH=/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/ADIOS2-2.10.1/bin:/home/openfoam_user/OpenFOAM/user-v2406/platforms/linux64GccDPInt32Opt/bin:/OpenFOAM-v2406/site/2406/platforms/linux64GccDPInt32Opt/bin:/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/bin:/OpenFOAM-v2406/bin:/OpenFOAM-v2406/wmake:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LD_LIBRARY_PATH=/home/openfoam_user/OpenFOAM/user-v2406/platforms/linux64GccDPInt32Opt/lib:/OpenFOAM-v2406/site/2406/platforms/linux64GccDPInt32Opt/lib:/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/lib/sys-openmpi:/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/lib:/OpenFOAM-v2406/ThirdParty/platforms/linux64GccDPInt32/lib/sys-openmpi:/OpenFOAM-v2406/ThirdParty/platforms/linux64GccDPInt32/lib:/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/fftw-3.3.10/lib:/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/CGAL-4.14.3/lib64:/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/boost_1_74_0/lib64:/OpenFOAM-v2406/ThirdParty/platforms/linux64Gcc/ADIOS2-2.10.1/lib:/usr/lib/x86_64-linux-gnu/openmpi/lib:/OpenFOAM-v2406/platforms/linux64GccDPInt32Opt/lib/dummy
