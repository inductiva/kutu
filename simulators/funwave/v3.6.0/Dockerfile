FROM inductiva/kutu:base-image_v0.1.1 as build

    # Fortran compiler
RUN wget https://github.com/fengyanshi/FUNWAVE-TVD/archive/refs/tags/Version_3.6.zip && \
    unzip Version_3.6.zip && \
    rm Version_3.6.zip && \
    cd FUNWAVE-TVD-Version_3.6/