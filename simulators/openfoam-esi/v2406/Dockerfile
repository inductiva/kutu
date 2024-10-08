FROM inductiva/kutu:base-image_v0.1.1_dev as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/openfoam-esi-input-example.zip -P /home/ && \
    unzip /home/openfoam-esi-input-example.zip -d /home/ && \
    rm /home/openfoam-esi-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1_dev as build

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

RUN wget https://dl.openfoam.com/source/v2406/OpenFOAM-v2406.tgz && \
	tar -xzf OpenFOAM-v2406.tgz && \
	cd OpenFOAM-v${openfoam_num_version} && \
	source etc/bashrc && \
    wget https://dl.openfoam.com/source/v2406/ThirdParty-v2406.tgz && \
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

# run as openfoam_user
RUN chmod +x /launch.sh && \
	cd /OpenFOAM-v2406 && \
	source etc/bashrc && \
	# This second Allwmake is necessary
	# https://www.cfd-online.com/Forums/openfoam-installation/100347-libscotch-so-missing.html
	./Allwmake -j && \
    rm -r /OpenFOAM-v2406/ThirdParty/build/ && \
    rm -r /OpenFOAM-v2406/build/ && \
    rm -r /OpenFOAM-v2406/ThirdParty/sources/
    #cant delete src folders because it might be needed to create new libraries
    #in some cases some libraries cannot be loaded so Openfoam creates them
    #on the fly (we need src for that)
