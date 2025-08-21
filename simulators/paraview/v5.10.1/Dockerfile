FROM ubuntu:22.04 as build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install paraview -y

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh