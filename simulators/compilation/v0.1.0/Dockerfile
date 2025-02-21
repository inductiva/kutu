# Use the official Ubuntu image as the base
FROM ubuntu:20.04

# Set the non-interactive mode to avoid prompts during installation
ARG DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    sudo \
    python && \
    pip install docker

# Install Docker
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh

# Add a user to avoid running Docker as root (optional)
RUN useradd -ms /bin/bash dockeruser && \
    usermod -aG sudo dockeruser

# Switch to the created user
USER dockeruser

# Set the working directory
WORKDIR /home/dockeruser

# Command to run Docker (to ensure Docker runs when the container starts)
CMD ["docker", "--version"]
