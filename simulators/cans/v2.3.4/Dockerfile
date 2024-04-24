FROM ubuntu:22.04 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/cans-input-example.zip -P /home/ && \
    unzip /home/cans-input-example.zip -d /home/cans-input-example && \
    rm /home/cans-input-example.zip && \
    ls -l

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM ubuntu:22.04 as build

RUN apt update -qq && \
    apt install -y build-essential && \
    apt install -y  openmpi-bin=4.1.2-2ubuntu1 \
        libopenmpi-dev=4.1.2-2ubuntu1 \
        libfftw3-dev \
        wget \
        git && \
    git clone --recursive --branch v2.3.4 https://github.com/CaNS-World/CaNS && \
    cd CaNS && \
    make libs && \
    make -j 4 && \
    cp -a /CaNS/run/* /usr/local/bin/ && \
    rm -r /CaNS


COPY --from=test_env /home /home