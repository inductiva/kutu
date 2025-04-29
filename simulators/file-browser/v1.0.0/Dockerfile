FROM ubuntu:22.04 as build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y curl \
    python3 \
    python3-pip \
    python3-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash && \
    curl -fsSL https://code-server.dev/install.sh | sh && \


COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh