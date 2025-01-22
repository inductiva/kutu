FROM ubuntu:focal as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/openfoam-input-example.zip -P /home/ && \
    unzip /home/openfoam-input-example.zip -d /home/ && \
    rm /home/openfoam-input-example.zip

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

ARG openfoam_num_version=12
ARG openfoam_version="openfoam${openfoam_num_version}"

# Install OpenFOAM from Foundation source (without ParaView)
# plus an extra environment variable to make OpenMPI play nice
RUN sh -c "wget -O - http://dl.openfoam.org/gpg.key | apt-key add -" ;\
	add-apt-repository http://dl.openfoam.org/ubuntu ;\
	apt-get update ;\
	apt-get install -y --no-install-recommends ${openfoam_version} ;\
	rm -rf /var/lib/apt/lists/*

ENV OPENFOAM_SOURCE_FILE=/opt/${openfoam_version}/etc/bashrc
COPY --from=test_env /home /home

ENV WM_CC="gcc"
ENV TERM="xterm"
ENV WM_CXX="g++"
ENV FOAM_SIGFPE=""
ENV FOAM_SETTINGS=""
ENV _="/usr/bin/env"
ENV WM_COMPILER="Gcc"
ENV WM_ARCH="linux64"
ENV WM_OSTYPE="POSIX"
ENV WM_LDFLAGS="-m64"
ENV ParaView_GL="mesa"
ENV WM_LABEL_SIZE="32"
ENV WM_ARCH_OPTION="64"
ENV ParaView_MAJOR="5.6"
ENV FOAM_INST_DIR="/opt"
ENV WM_PROJECT="OpenFOAM"
ENV WM_CFLAGS="-m64 -fPIC"
ENV WM_LINK_LANGUAGE="c++"
ENV WM_PROJECT_VERSION="12"
ENV HOSTNAME="a3ada66b4e2c"
ENV WM_LABEL_OPTION="Int32"
ENV WM_COMPILE_OPTION="Opt"
ENV WM_PRECISION_OPTION="DP"
ENV WM_MPLIB="SYSTEMOPENMPI"
ENV ParaView_VERSION="5.6.0"
ENV FOAM_MPI="openmpi-system"
ENV WM_COMPILER_TYPE="system"
ENV WM_COMPILER_LIB_ARCH="64"
ENV WM_PROJECT_INST_DIR="/opt"
ENV MPI_BUFFER_SIZE="20000000"
ENV FOAM_ETC="/opt/openfoam12/etc"
ENV WM_DIR="/opt/openfoam12/wmake"
ENV FOAM_SRC="/opt/openfoam12/src"
ENV FOAM_JOB_DIR="/opt/jobControl"
ENV WM_PROJECT_DIR="/opt/openfoam12"
ENV FOAM_RUN="/root/OpenFOAM/-8/run"
ENV DEBIAN_FRONTEND="noninteractive"
ENV WM_OPTIONS="linux64GccDPInt32Opt"
ENV LESSOPEN="| /usr/bin/lesspipe %s"
ENV LESSCLOSE="/usr/bin/lesspipe %s %s"
ENV WM_CXXFLAGS="-m64 -fPIC -std=c++0x"
ENV WM_THIRD_PARTY_DIR="/opt/ThirdParty-8"
ENV ParaView_DIR="/opt/paraviewopenfoam56"
ENV FOAM_APP="/opt/openfoam12/applications"
ENV WM_PROJECT_USER_DIR="/root/OpenFOAM/-8"
ENV FOAM_TUTORIALS="/opt/openfoam12/tutorials"
ENV OPENFOAM_SOURCE_FILE="/opt/openfoam12/etc/bashrc"
ENV MPI_ARCH_PATH="/usr/lib/x86_64-linux-gnu/openmpi"
ENV FOAM_SOLVERS="/opt/openfoam12/applications/solvers"
ENV FOAM_UTILITIES="/opt/openfoam12/applications/utilities"
ENV FOAM_APPBIN="/opt/openfoam12/platforms/linux64GccDPInt32Opt/bin"
ENV FOAM_LIBBIN="/opt/openfoam12/platforms/linux64GccDPInt32Opt/lib"
ENV FOAM_SITE_LIBBIN="/opt/site/8/platforms/linux64GccDPInt32Opt/lib"
ENV FOAM_SITE_APPBIN="/opt/site/8/platforms/linux64GccDPInt32Opt/bin"
ENV FOAM_EXT_LIBBIN="/opt/ThirdParty-8/platforms/linux64GccDPInt32/lib"
ENV FOAM_USER_LIBBIN="/root/OpenFOAM/-8/platforms/linux64GccDPInt32Opt/lib"
ENV FOAM_USER_APPBIN="/root/OpenFOAM/-8/platforms/linux64GccDPInt32Opt/bin"
ENV PATH="/opt/ThirdParty-8/platforms/linux64Gcc/gperftools-svn/bin:/root/OpenFOAM/-8/platforms/linux64GccDPInt32Opt/bin:/opt/site/8/platforms/linux64GccDPInt32Opt/bin:/opt/openfoam12/platforms/linux64GccDPInt32Opt/bin:/opt/openfoam12/bin:/opt/openfoam12/wmake:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV LD_LIBRARY_PATH="/opt/ThirdParty-8/platforms/linux64Gcc/gperftools-svn/lib:/opt/openfoam12/platforms/linux64GccDPInt32Opt/lib/openmpi-system:/opt/ThirdParty-8/platforms/linux64GccDPInt32/lib/openmpi-system:/usr/lib/x86_64-linux-gnu/openmpi/lib:/root/OpenFOAM/-8/platforms/linux64GccDPInt32Opt/lib:/opt/site/8/platforms/linux64GccDPInt32Opt/lib:/opt/openfoam12/platforms/linux64GccDPInt32Opt/lib:/opt/ThirdParty-8/platforms/linux64GccDPInt32/lib:/opt/openfoam12/platforms/linux64GccDPInt32Opt/lib/dummy"

COPY ./functions/* /bin/

RUN chmod +x /bin/*