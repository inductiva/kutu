FROM ubuntu:22.04 as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/openfoam-esi-input-example.zip -P /home/ && \
    unzip /home/openfoam-esi-input-example.zip -d /home/ && \
    rm /home/openfoam-esi-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Start from the official Ubuntu Bionic (18.04 LTS) image
FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

# Install any extra things we might need
RUN apt-get update \
	&& apt-get install -y \
	vim \
	ssh \
	git \
	wget \
	gmsh \
	software-properties-common ;\
	rm -rf /var/lib/apt/lists/*

ARG openfoam_num_version=2206
ARG openfoam_version="openfoam${openfoam_num_version}"

# Install OpenFOAM from Esi (without ParaView)
# plus an extra environment variable to make OpenMPI play nice
RUN sh -c "wget -O - http://dl.openfoam.com/add-debian-repo.sh | bash" ;\
	apt-get update ;\
	apt-get install -y --no-install-recommends ${openfoam_version} ;\
	rm -rf /var/lib/apt/lists/*

ENV OPENFOAM_SOURCE_FILE=/usr/lib/openfoam/${openfoam_version}/etc/bashrc
COPY --from=test_env /home /home
COPY ./launch.sh /launch.sh
RUN chmod +x /launch.sh

ENV FOAM_API=2206
ENV WM_COMPILER=Gcc
ENV WM_ARCH=linux64
ENV WM_LABEL_SIZE=32
ENV WM_PROJECT=OpenFOAM
ENV FOAM_MPI=sys-openmpi
ENV WM_LABEL_OPTION=Int32
ENV WM_COMPILE_OPTION=Opt
ENV WM_PRECISION_OPTION=DP
ENV WM_MPLIB=SYSTEMOPENMPI
ENV WM_COMPILER_TYPE=system
ENV WM_COMPILER_LIB_ARCH=64
ENV WM_PROJECT_VERSION=v2206
ENV WM_OPTIONS=linux64GccDPInt32Opt
ENV FOAM_RUN=/root/OpenFOAM/user-v2206/run
ENV FOAM_ETC=/usr/lib/openfoam/openfoam2206/etc
ENV FOAM_SRC=/usr/lib/openfoam/openfoam2206/src
ENV WM_PROJECT_USER_DIR=/root/OpenFOAM/user-v2206
ENV WM_PROJECT_DIR=/usr/lib/openfoam/openfoam2206
ENV MPI_ARCH_PATH=/usr/lib/x86_64-linux-gnu/openmpi
ENV FOAM_APP=/usr/lib/openfoam/openfoam2206/applications
ENV FOAM_TUTORIALS=/usr/lib/openfoam/openfoam2206/tutorials
ENV WM_THIRD_PARTY_DIR=/usr/lib/openfoam/openfoam2206/ThirdParty
ENV OPENFOAM_SOURCE_FILE=/usr/lib/openfoam/openfoam2206/etc/bashrc
ENV FOAM_SOLVERS=/usr/lib/openfoam/openfoam2206/applications/solvers
ENV FOAM_UTILITIES=/usr/lib/openfoam/openfoam2206/applications/utilities
ENV FOAM_APPBIN=/usr/lib/openfoam/openfoam2206/platforms/linux64GccDPInt32Opt/bin
ENV FOAM_LIBBIN=/usr/lib/openfoam/openfoam2206/platforms/linux64GccDPInt32Opt/lib
ENV FOAM_USER_LIBBIN=/root/OpenFOAM/user-v2206/platforms/linux64GccDPInt32Opt/lib
ENV FOAM_USER_APPBIN=/root/OpenFOAM/user-v2206/platforms/linux64GccDPInt32Opt/bin
ENV CGAL_ARCH_PATH=/usr/lib/openfoam/openfoam2206/ThirdParty/platforms/linux64Gcc/cgal-system
ENV FFTW_ARCH_PATH=/usr/lib/openfoam/openfoam2206/ThirdParty/platforms/linux64Gcc/fftw-system
ENV BOOST_ARCH_PATH=/usr/lib/openfoam/openfoam2206/ThirdParty/platforms/linux64Gcc/boost-system
ENV FOAM_SITE_LIBBIN=/usr/lib/openfoam/openfoam2206/site/2206/platforms/linux64GccDPInt32Opt/lib
ENV ADIOS2_ARCH_PATH=/usr/lib/openfoam/openfoam2206/ThirdParty/platforms/linux64Gcc/ADIOS2-2.7.1
ENV FOAM_SITE_APPBIN=/usr/lib/openfoam/openfoam2206/site/2206/platforms/linux64GccDPInt32Opt/bin
ENV SCOTCH_ARCH_PATH=/usr/lib/openfoam/openfoam2206/ThirdParty/platforms/linux64GccDPInt32/scotch-system
ENV PATH=/usr/lib/x86_64-linux-gnu/openmpi/bin:/root/OpenFOAM/user-v2206/platforms/linux64GccDPInt32Opt/bin:/usr/lib/openfoam/openfoam2206/site/2206/platforms/linux64GccDPInt32Opt/bin:/usr/lib/openfoam/openfoam2206/platforms/linux64GccDPInt32Opt/bin:/usr/lib/openfoam/openfoam2206/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LD_LIBRARY_PATH=/root/OpenFOAM/user-v2206/platforms/linux64GccDPInt32Opt/lib:/usr/lib/openfoam/openfoam2206/site/2206/platforms/linux64GccDPInt32Opt/lib:/usr/lib/openfoam/openfoam2206/platforms/linux64GccDPInt32Opt/lib/sys-openmpi:/usr/lib/openfoam/openfoam2206/platforms/linux64GccDPInt32Opt/lib:/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/openfoam/openfoam2206/platforms/linux64GccDPInt32Opt/lib/dummy