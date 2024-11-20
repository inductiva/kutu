FROM inductiva/kutu:base-image_v0.1.1 as build

ENV WWATCH3_NETCDF=NC4
ENV NETCDF_CONFIG=/usr/bin/nc-config
ENV EXTRA_COMP_OPTIONS="-fallow-argument-mismatch"
ENV WW3=/WW3-6.07.1

RUN apt install ssh rsync -y && \
    wget https://github.com/NOAA-EMC/WW3/archive/refs/tags/6.07.1.tar.gz && \
    tar -xvf 6.07.1.tar.gz && \
    cd WW3-6.07.1/ && \
    echo -e ".\nn\nn" | sh model/bin/ww3_from_ftp.sh && \
    echo -e "n" | ./model/bin/w3_setup /WW3-6.07.1/model/ -c Gnu -s Ifremer2 && \
    ./model/bin/w3_automake
    
