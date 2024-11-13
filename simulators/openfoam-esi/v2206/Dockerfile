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
ENV FOAM_EXT_LIBBIN=/OpenFOAM-v2206/platforms/linux64GccDPInt32Opt/lib/

ARG openfoam_num_version=2206
ARG openfoam_version="openfoam${openfoam_num_version}"

RUN apt-get update && \
	apt install -y paraview-dev \
        cmake qtbase5-dev qttools5-dev \
        qttools5-dev-tools libqt5opengl5-dev \
        libqt5x11extras5-dev libxt-dev flex

RUN wget "https://altushost-swe.dl.sourceforge.net/project/openfoam/v2206/OpenFOAM-v2206.tgz?viasf=1" -O OpenFOAM-v2206.tgz && \
	tar -xzf OpenFOAM-v2206.tgz && \
	cd OpenFOAM-v${openfoam_num_version} && \
	source etc/bashrc && \
    wget "https://deac-fra.dl.sourceforge.net/project/openfoam/v2206/ThirdParty-v2206.tgz?viasf=1" -O ThirdParty-v2206.tgz && \
	tar -xzf ThirdParty-v2206.tgz && \
	mv ThirdParty-v2206 ThirdParty && \
    rm /OpenFOAM-v2206/ThirdParty-v2206.tgz && \
	./Allwmake -j

FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

ENV OPENFOAM_SOURCE_FILE=/OpenFOAM-v2206/etc/bashrc
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

COPY --from=build --chown=openfoam_user /OpenFOAM-v2206 /OpenFOAM-v2206
COPY --from=test_env --chown=openfoam_user /home /home
COPY --chown=openfoam_user ./launch.sh /launch.sh

# run as openfoam_user
RUN chmod +x /launch.sh && \
	cd /OpenFOAM-v2206 && \
	source etc/bashrc && \
	# This second Allwmake is necessary
	# https://www.cfd-online.com/Forums/openfoam-installation/100347-libscotch-so-missing.html
	./Allwmake -j && \
    rm -r /OpenFOAM-v2206/ThirdParty/build/ && \
    rm -r /OpenFOAM-v2206/build/ && \
    rm -r /OpenFOAM-v2206/ThirdParty/sources/
    #cant delete src folders because it might be needed to create new libraries
    #in some cases some libraries cannot be loaded so Openfoam creates them
    #on the fly (we need src for that)


ENTRYPOINT ["/bin/bash", "-c", "bash /OpenFOAM-v2206/etc/bashrc && bash /OpenFOAM-v2206/bin/tools/RunFunctions && exec \"$@\""]