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
