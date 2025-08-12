FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/calculix-input-example.zip -P /home/ && \
    unzip /home/calculix-input-example.zip -d /home/ && \
    rm /home/calculix-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

FROM ubuntu:18.04 as build

RUN apt-get update && \
    apt-get install -y wget bzip2 unzip libgomp1 libgfortran4 libglu1-mesa libxi6 libxmu6 libxmu-dev libxi-dev build-essential \
    libgl1-mesa-dev libglew-dev && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://www.dhondt.de/ccx_2.22.tar.bz2 && \
    tar -xjf ccx_2.22.tar.bz2 && \
    cd CalculiX/ccx_2.22/src && \
    cp ccx_2.22 /bin/ccx

RUN wget https://www.dhondt.de/cgx_2.22.all.tar.bz2 && \
    tar -xjf cgx_2.22.all.tar.bz2 && \
    mv CalculiX /usr/local/CalculiX && \
    cd /usr/local/CalculiX/cgx_2.22/src && \
    make && \
    cp cgx /bin/cgx

COPY --from=test_env /home /home

