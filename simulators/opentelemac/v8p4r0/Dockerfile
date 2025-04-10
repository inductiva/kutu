FROM ubuntu:22.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential gfortran mpich git wget curl \
    python3 python3-pip python3-numpy python3-scipy python3-matplotlib \
    libmetis-dev cmake unzip git-lfs && git lfs install

WORKDIR /opt
RUN git clone https://gitlab.pam-retd.fr/otm/telemac-mascaret.git telemac-mascaret

WORKDIR /opt/telemac-mascaret
RUN git checkout tags/v8p4r0 && git lfs pull

# Copy configs
COPY systel.cfg /opt/telemac-mascaret/configs/systel.cfg
COPY pysource.sh /opt/telemac-mascaret/configs/pysource.sh

# Build TELEMAC
ENV SOURCEFILE=/opt/telemac-mascaret/configs/pysource.sh
RUN bash -c "source $SOURCEFILE && compile_telemac.py"


FROM ubuntu:22.04 as final

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 python3-pip libmetis-dev mpich \
    python3-numpy python3-scipy python3-matplotlib && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/telemac-mascaret/scripts /opt/telemac-mascaret/scripts
COPY --from=builder /opt/telemac-mascaret/builds /opt/telemac-mascaret/builds
COPY --from=builder /opt/telemac-mascaret/configs /opt/telemac-mascaret/configs
COPY --from=builder /opt/telemac-mascaret/sources /opt/telemac-mascaret/sources

ENV HOMETEL=/opt/telemac-mascaret
ENV SYSTELCFG=$HOMETEL/configs/systel.cfg
ENV USETELCFG=gfortranHPC
ENV SOURCEFILE=$HOMETEL/configs/pysource.sh
ENV PATH=$HOMETEL/scripts/python3:$PATH
ENV PYTHONPATH=$HOMETEL/scripts/python3:$HOMETEL/builds/$USETELCFG/wrap_api/lib:$PYTHONPATH
ENV LD_LIBRARY_PATH=$HOMETEL/builds/$USETELCFG/lib:$HOMETEL/builds/$USETELCFG/wrap_api/lib:$LD_LIBRARY_PATH
ENV PYTHONUNBUFFERED=true

WORKDIR /case
VOLUME /case

# Get input example
RUN wget -O /home/opentelemac-input-example.zip https://storage.googleapis.com/inductiva-api-demo-files/opentelemac-input-example.zip \
    && unzip /home/opentelemac-input-example.zip -d /home/ \
    && rm /home/opentelemac-input-example.zip \
    # Reduce Simulation time to 1 second
    && sed -i 's/^DURATION *= *.*/DURATION = 1./' /home/t2d_malpasset-fine.cas

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

CMD ["bash"]
