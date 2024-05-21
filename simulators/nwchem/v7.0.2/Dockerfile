FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN apt-get update && apt-get install -y \
    wget \
    unzip && \
    wget https://storage.googleapis.com/inductiva-api-demo-files/nwchem-input-example.zip -P /home/ && \
    unzip /home/nwchem-input-example.zip -d /home/ && \
    rm /home/nwchem-input-example.zip && \
    ls -l

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.0 as build

RUN apt-get  install -y nwchem=7.0.2-3

COPY --from=test_env /home /home
