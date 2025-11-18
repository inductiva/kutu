FROM ubuntu:22.04 AS build

ARG DEBIAN_FRONTEND=noninteractive
ARG SWMM_VERSION=5.2.4
ARG SWMM_SRC_URL=https://www.epa.gov/system/files/other-files/2023-08/swmm524_engine.zip

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        cmake \
        python3 \
        wget \
        unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/swmm

RUN wget -O swmm.zip ${SWMM_SRC_URL} && \
    unzip -q swmm.zip && \
    mv swmm524_engine swmm-${SWMM_VERSION} && \
    rm swmm.zip

WORKDIR /tmp/swmm/swmm-${SWMM_VERSION}

RUN python3 - <<'PY'
from pathlib import Path
path = Path("src/consts.h")
old = "#define   MAXFNAME           259            // Max. # characters in file name"
new = "#define   MAXFNAME           1023           // Max. # characters in file name"
text = path.read_text()
if old not in text:
    raise SystemExit("MAXFNAME definition not found")
path.write_text(text.replace(old, new, 1))
PY

RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && \
    cmake --build build -j"$(nproc)" && \
    install -d /opt/swmm/bin /opt/swmm/lib && \
    cp build/runswmm /opt/swmm/bin/ && \
    cp build/libswmm5.so /opt/swmm/lib/

FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
        libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/swmm /opt/swmm

RUN printf '/opt/swmm/lib\n' > /etc/ld.so.conf.d/swmm.conf && \
    ldconfig

ENV PATH="/opt/swmm/bin:${PATH}"

RUN ln -s /opt/swmm/bin/runswmm /usr/local/bin/runswmm

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh
