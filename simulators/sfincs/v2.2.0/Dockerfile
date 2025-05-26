FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/sfincs-input-example.zip -P /home/ && \
    unzip /home/sfincs-input-example.zip -d /home/ && \
    rm /home/sfincs-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM deltares/sfincs-cpu@sha256:5f36f93b4e767fa62326ca91e5cf2a78d5da2285b8adc7dbb59ae06b6c19cf12 as build

COPY --from=test_env /home /home