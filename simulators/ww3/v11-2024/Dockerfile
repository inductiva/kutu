FROM inductiva/kutu:base-image_v0.1.1 as build

ENV WWATCH3_NETCDF=NC4
ENV NETCDF_CONFIG=/usr/bin/nc-config
ENV EXTRA_COMP_OPTIONS="-fallow-argument-mismatch"
ENV WW3=/WW3

RUN apt install ssh rsync -y && \
    git clone https://github.com/NOAA-EMC/WW3.git && \
    cd WW3/ && \
    git checkout 7705171721e825d58e1e867e552e328fc812bfdd && \
    echo -e ".\nn\nn" | sh model/bin/ww3_from_ftp.sh && \
    mkdir build && \
    cd build/ && \
    cmake .. -DSWITCH=Ifremer2  && \
    make -j && \
    make install