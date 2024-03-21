# Start from an official GROMACS image from GROMACS.
FROM gromacs/gromacs:2022.2 as build

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/gromacs-input-example.zip -P /home/ && \
    unzip /home/gromacs-input-example.zip -d /home/
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Start from a clen GROMACS image
FROM gromacs/gromacs:2022.2

# Set environment variable to allow GPU direct communication
ENV GMX_ENABLE_DIRECT_GPU_COMM=1

COPY --from=build /home /home