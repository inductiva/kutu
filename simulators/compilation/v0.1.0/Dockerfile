FROM docker:cli

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python && \
    pip install docker