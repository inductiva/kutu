FROM pawannegi/openfoam24-cfmesh:latest

# Set up environment variables for OpenFOAM
ENV FOAM_RUN=/workdir/output/artifacts/__customCode__/Openfoam/user-v2412/run
ENV WM_PROJECT_USER_DIR=/workdir/output/artifacts/__customCode__/Openfoam/user-v2412
ENV WM_PROJECT=OpenFOAM
ENV WM_PROJECT_VERSION=v2412
ENV FOAM_API="2412"
ENV FOAM_MPI="sys-openmpi"
ENV WM_COMPILER="Gcc"
ENV WM_COMPILER_TYPE="system"
ENV WM_COMPILER_LIB_ARCH="64"
ENV WM_ARCH="linux64"
ENV WM_MPLIB="SYSTEMOPENMPI"
ENV WM_LABEL_SIZE="32"
ENV WM_LABEL_OPTION="Int32"
ENV WM_COMPILE_OPTION="Opt"
ENV WM_PRECISION_OPTION="DP"
ENV WM_OPTIONS="linux64GccDPInt32Opt"
ENV WM_PROJECT_DIR="/usr/lib/openfoam/openfoam2412"
ENV WM_DIR="/usr/lib/openfoam/openfoam2412/wmake"
ENV WM_THIRD_PARTY_DIR="/usr/lib/openfoam/openfoam2412/ThirdParty"
ENV MPI_ARCH_PATH="/usr/lib/x86_64-linux-gnu/openmpi"
ENV FOAM_ETC="/usr/lib/openfoam/openfoam2412/etc"
ENV FOAM_SRC="/usr/lib/openfoam/openfoam2412/src"
ENV FOAM_TUTORIALS="/usr/lib/openfoam/openfoam2412/tutorials"
ENV FOAM_APP="/usr/lib/openfoam/openfoam2412/applications"
ENV FOAM_SOLVERS="/usr/lib/openfoam/openfoam2412/applications/solvers"
ENV FOAM_UTILITIES="/usr/lib/openfoam/openfoam2412/applications/utilities"
ENV FOAM_APPBIN="/usr/lib/openfoam/openfoam2412/platforms/linux64GccDPInt32Opt/bin"
ENV FOAM_LIBBIN="/usr/lib/openfoam/openfoam2412/platforms/linux64GccDPInt32Opt/lib"
ENV FOAM_SITE_APPBIN="/usr/lib/openfoam/openfoam2412/site/2412/platforms/linux64GccDPInt32Opt/bin"
ENV FOAM_SITE_LIBBIN="/usr/lib/openfoam/openfoam2412/site/2412/platforms/linux64GccDPInt32Opt/lib"
ENV FOAM_USER_APPBIN="/root/OpenFOAM/user-v2412/platforms/linux64GccDPInt32Opt/bin"
ENV FOAM_USER_LIBBIN="/root/OpenFOAM/user-v2412/platforms/linux64GccDPInt32Opt/lib"
ENV CFMESH_DIR="/root/OpenFOAM/user-v2412/platforms/linux64GccDPInt32Opt"
ENV CGAL_ARCH_PATH="/usr/lib/openfoam/openfoam2412/ThirdParty/platforms/linux64Gcc/cgal-system"
ENV FFTW_ARCH_PATH="/usr/lib/openfoam/openfoam2412/ThirdParty/platforms/linux64Gcc/fftw-system"
ENV BOOST_ARCH_PATH="/usr/lib/openfoam/openfoam2412/ThirdParty/platforms/linux64Gcc/boost-system"
ENV ADIOS2_ARCH_PATH="/usr/lib/openfoam/openfoam2412/ThirdParty/platforms/linux64Gcc/ADIOS2-2.10.1"
ENV SCOTCH_ARCH_PATH="/usr/lib/openfoam/openfoam2412/ThirdParty/platforms/linux64GccDPInt32/scotch-system"

# Add cfMesh tools to PATH
ENV PATH="/usr/lib/x86_64-linux-gnu/openmpi/bin:/root/OpenFOAM/user-v2412/platforms/linux64GccDPInt32Opt/bin:/usr/lib/openfoam/openfoam2412/site/2412/platforms/linux64GccDPInt32Opt/bin:/usr/lib/openfoam/openfoam2412/platforms/linux64GccDPInt32Opt/bin:/usr/lib/openfoam/openfoam2412/bin:/usr/lib/openfoam/openfoam2412/wmake:${PATH}"
ENV LD_LIBRARY_PATH="/root/OpenFOAM/user-v2412/platforms/linux64GccDPInt32Opt/lib:/usr/lib/openfoam/openfoam2412/site/2412/platforms/linux64GccDPInt32Opt/lib:/usr/lib/openfoam/openfoam2412/platforms/linux64GccDPInt32Opt/lib/sys-openmpi:/usr/lib/openfoam/openfoam2412/platforms/linux64GccDPInt32Opt/lib:/usr/lib/x86_64-linux-gnu/openmpi/lib:/usr/lib/openfoam/openfoam2412/platforms/linux64GccDPInt32Opt/lib/dummy:${LD_LIBRARY_PATH}"

# Create work directory
RUN mkdir -p /workdir/output/artifacts/__customCode__/Openfoam/user-v2412/run
RUN mkdir -p /home && ln -s /root/OpenFOAM /home/OpenFOAM

# Copy and set up test script
COPY ./test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

WORKDIR /workdir

