FROM pawannegi/openfoam24-cfmesh:latest

# Set up environment variables for OpenFOAM
ENV FOAM_RUN=/workdir/output/artifacts/__customCode__/Openfoam/user-v2412/run
ENV WM_PROJECT_USER_DIR=/workdir/output/artifacts/__customCode__/Openfoam/user-v2412
ENV WM_PROJECT=OpenFOAM
ENV WM_PROJECT_VERSION=v2412
ENV FOAM_API="2412"
ENV WM_COMPILER="Gcc"
ENV WM_ARCH="linux64"
ENV WM_LABEL_SIZE="32"
ENV WM_LABEL_OPTION="Int32"
ENV WM_COMPILE_OPTION="Opt"
ENV WM_PRECISION_OPTION="DP"
ENV WM_OPTIONS="linux64GccDPInt32Opt"

# Add cfMesh tools to PATH
ENV PATH="/root/OpenFOAM/user-v2412/platforms/linux64GccDPInt32Opt/bin:${PATH}"

# Create work directory
RUN mkdir -p /workdir/output/artifacts/__customCode__/Openfoam/user-v2412/run

# Copy and set up test script
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

WORKDIR /workdir

