FROM ubuntu:22.04 as build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
    
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh