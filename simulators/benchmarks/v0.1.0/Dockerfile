# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set non-interactive mode for apt-get to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    curl \
    gcc \
    g++ \
    make \
    git \
    && rm -rf /var/lib/apt/lists/* && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    python3.12 -m pip install --upgrade pip && \
    python3.12 -m pip install plotly inductiva

