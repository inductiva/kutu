FROM inductiva/kutu:base-image_v0.1.1 as build

RUN wget https://github.com/NOAA-EMC/WW3/archive/refs/tags/6.07.1.tar.gz && \
    tar -xvf 6.07.1.tar.gz && \
    cd WW3-6.07.1/ && \
    echo -e ".\nn\nn" | sh model/bin/ww3_from_ftp.sh
