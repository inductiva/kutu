FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/sfincs-input-example.zip -P /home/ && \
    unzip /home/sfincs-input-example.zip -d /home/ && \
    rm /home/sfincs-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM deltares/sfincs-cpu:sfincs-v2.1.3 as test_env

COPY --from=test_env /home /home