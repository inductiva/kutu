FROM ubuntu:22.04 as test_env

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip &&\
    wget https://storage.googleapis.com/inductiva-api-demo-files/splishsplash-input-example.zip -P /home/ && \
    unzip /home/splishsplash-input-example.zip -d /home/ && \
    rm /home/splishsplash-input-example.zip

COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Start from an official CUDA image from NVIDIA.
FROM ubuntu:22.04 as build

# Set frontend to be noninteractive, to avoid prompts during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install SPlisHSPlasH dependencies.
RUN apt-get update -y; \
    apt-get install -y git cmake xorg-dev freeglut3-dev build-essential

# Install Python 3.11.
RUN apt-get update -y; \
    apt-get install curl software-properties-common -y; \
    add-apt-repository ppa:deadsnakes/ppa; \
    apt-get install -y python3.11 python3.11-distutils; \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11; \
    rm -f /usr/bin/python && ln -s /usr/bin/python3.11 /usr/bin/python


# Clone SPlisHSPlasH repository.
WORKDIR /
RUN git clone https://github.com/InteractiveComputerGraphics/SPlisHSPlasH.git

RUN cmake \
    -S /SPlisHSPlasH -B /SPlisHSPlasH_CPU/build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE=/SPlisHSPlasH_CPU/bin \
    -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=/SPlisHSPlasH_CPU/bin \
    -DUSE_PYTHON_BINDINGS=OFF \
    -DBuild_PartioViewer=OFF \
    -DBuild_FoamGenerator=OFF \
    -DBuild_VolumeSampling=OFF \
    -DBuild_MeshSkinning=OFF

WORKDIR /SPlisHSPlasH_CPU/build
RUN make -j 4

# Install gmsh.
RUN apt-get update -y; \
    apt-get install -y gmsh

RUN apt-get update && apt-get install -y \
    curl && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    /root/.cargo/bin/cargo install splashsurf

FROM ubuntu:22.04 

ENV PATH="/root/.cargo/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libosmesa6 \
    libosmesa6-dev \
    libxrender1 && \
    pip3 install --no-cache-dir \
    numpy \
    imageio \
    vtk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./gen_gif.py /home/scripts/gen_gif.py

COPY --from=build /root/.cargo/bin/splashsurf /root/.cargo/bin/splashsurf

COPY --from=build /usr/lib/x86_64-linux-gnu/libGLdispatch.so.0 /usr/lib/x86_64-linux-gnu/libGLdispatch.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0 /usr/lib/x86_64-linux-gnu/libgomp.so.1.0.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libX11.so.6.4.0 /usr/lib/x86_64-linux-gnu/libX11.so.6.4.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libGLU.so.1.3.1 /usr/lib/x86_64-linux-gnu/libGLU.so.1.3.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libOpenGL.so.0 /usr/lib/x86_64-linux-gnu/libOpenGL.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libXdmcp.so.6 /usr/lib/x86_64-linux-gnu/libXdmcp.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libX11.so.6 /usr/lib/x86_64-linux-gnu/libX11.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libGLU.so.1 /usr/lib/x86_64-linux-gnu/libGLU.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libxcb.so.1 /usr/lib/x86_64-linux-gnu/libxcb.so.1
COPY --from=build /usr/lib/x86_64-linux-gnu/libXau.so.6 /usr/lib/x86_64-linux-gnu/libXau.so.6
COPY --from=build /usr/lib/x86_64-linux-gnu/libbsd.so.0 /usr/lib/x86_64-linux-gnu/libbsd.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libmd.so.0 /usr/lib/x86_64-linux-gnu/libmd.so.0
COPY --from=build /usr/lib/x86_64-linux-gnu/libX11.so /usr/lib/x86_64-linux-gnu/libX11.so
COPY --from=build /usr/lib/x86_64-linux-gnu/libX11.a /usr/lib/x86_64-linux-gnu/libX11.a

COPY --from=build /SPlisHSPlasH_CPU/bin /SPlisHSPlasH_CPU/bin
COPY --from=test_env /home /home
