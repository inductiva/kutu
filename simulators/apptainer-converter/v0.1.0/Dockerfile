FROM ubuntu:22.04

RUN apt-get update && apt-get install -y wget

# Build and install Apptainer
RUN cd /tmp \
    && wget https://github.com/apptainer/apptainer/releases/download/v1.3.3/apptainer_1.3.3_amd64.deb \
    && apt-get install -y ./apptainer_1.3.3_amd64.deb \
    && rm /tmp/*

WORKDIR /build

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

ENTRYPOINT ["apptainer"]
