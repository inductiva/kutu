# Stage 1: Prepare the test environment
FROM ubuntu:22.04 as test_env

# Set frontend to be noninteractive to avoid prompts during installations
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies for test environment
RUN apt-get update && apt-get install -y \
    wget \
    git \
    unzip

# Set up directories for examples and output
RUN mkdir -p /home/seissol/examples /home/seissol/output

# Clone SeisSol examples repository
RUN git clone https://github.com/SeisSol/Examples.git /home/seissol/examples

# Download specific test data for tpv33 example
WORKDIR /home/seissol/examples/tpv33
RUN wget https://zenodo.org/record/8042664/files/tpv33_half_sym.xdmf -O tpv33_half_sym.xdmf && \
    wget https://zenodo.org/record/8042664/files/tpv33_half_sym -O tpv33_half_sym

# Copy test simulation script into the container
COPY ./test_sim.sh /home/seissol/examples/tpv33/test_sim.sh
RUN chmod +x /home/seissol/examples/tpv33/test_sim.sh

# Stage 2: Build the SeisSol environment
FROM seissol/training:latest as build

# Set environment variables for consistency
ENV DEBIAN_FRONTEND=noninteractive
ENV SEISSOL_COMMTHREAD=0
ENV PATH="/usr/local/bin:/home/tools/bin:$PATH"

# Install additional tools and Python dependencies
RUN apt-get update && apt-get install -y \
    nano \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install numpy scipy matplotlib


COPY --from=test_env /home /home
# Set the working directory
WORKDIR /home/seissol/examples/tpv33

# Ensure the test script is executable
RUN chmod +x /home/seissol/examples/tpv33/test_sim.sh
# Expose the port for JupyterLab
EXPOSE 53155
# Default command to execute the test script
CMD ["/home/seissol/examples/tpv33/test_sim.sh"]





