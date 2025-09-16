FROM inductiva/kutu:base-image_v0.1.0 as test_env

RUN wget https://storage.googleapis.com/inductiva-api-demo-files/funwave-input-example.zip -P /home/ && \
    unzip /home/funwave-input-example.zip -d /home/ && \
    rm /home/funwave-input-example.zip 

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

FROM inductiva/kutu:base-image_v0.1.1 as build

    # Fortran compiler
RUN wget https://github.com/fengyanshi/FUNWAVE-TVD/archive/refs/tags/Version_3.6.zip && \
    unzip Version_3.6.zip && \
    rm Version_3.6.zip && \
    sed -i 's|^FUNWAVE_DIR *= .*|FUNWAVE_DIR = /FUNWAVE-TVD-Version_3.6|; s|^COMPILER *= intel|COMPILER    = gnu|' /FUNWAVE-TVD-Version_3.6/Makefile && \
    sed -i 's/^EXEC\s*=\s*funwave$/EXEC        = compiled_funwave/' /FUNWAVE-TVD-Version_3.6/Makefile && \
    cd /FUNWAVE-TVD-Version_3.6 && \
    make

COPY --from=test_env /home /home