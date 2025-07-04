FROM ubuntu:22.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    build-essential gfortran-9 git wget curl \
    openmpi-bin=4.1.2-2ubuntu1 openmpi-common=4.1.2-2ubuntu1 \
    libopenmpi-dev=4.1.2-2ubuntu1 \
    python3 python3-pip python3-numpy python3-scipy python3-matplotlib \
    libmetis-dev cmake unzip && \
    update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-9 100


WORKDIR /opt
RUN git clone https://gitlab.pam-retd.fr/otm/telemac-mascaret.git telemac-mascaret

WORKDIR /opt/telemac-mascaret
RUN git checkout tags/v8p1r2

# Copy configs
COPY systel.cfg /opt/telemac-mascaret/configs/systel.cfg
COPY pysource.sh /opt/telemac-mascaret/configs/pysource.sh

# Build TELEMAC
ENV SOURCEFILE=/opt/telemac-mascaret/configs/pysource.sh
RUN bash -c "source $SOURCEFILE && compile_telemac.py"


FROM ubuntu:22.04 as final

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 python3-pip libmetis-dev \
    openmpi-bin=4.1.2-2ubuntu1 openmpi-common=4.1.2-2ubuntu1 \
    libopenmpi-dev=4.1.2-2ubuntu1 \
    python3-numpy python3-scipy python3-matplotlib curl unzip && \
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
ENV OMPI_ALLOW_RUN_AS_ROOT=1
ENV OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1


WORKDIR /case
VOLUME /case

# Get input example
RUN curl https://storage.googleapis.com/inductiva-api-demo-files/opentelemac-v8p1r2-input-example.zip \
    --output /home/opentelemac-v8p1r2-input-example.zip \
    && unzip /home/opentelemac-v8p1r2-input-example.zip -d /home/ \
    && rm /home/opentelemac-v8p1r2-input-example.zip \
    # Reduce Simulation time to 5 second for testing
    && sed -i 's/^DURATION *= *.*/DURATION = 5./' /home/opentelemac-v8p1r2-input-example/t2d_malpasset-fine.cas

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

CMD ["bash"]
