# Use the official Ubuntu base image
FROM python:3.12.8

# Set non-interactive mode for apt-get to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN pip install plotly inductiva

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh