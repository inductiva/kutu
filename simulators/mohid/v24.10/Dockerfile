# Base image
FROM ubuntu:22.04 AS base

# Metadata about the image
LABEL maintainer="Joao Rodrigues <joao.rodrigues@hidromod.com>"
LABEL version="1.0"
LABEL created="2024-11-18"
LABEL revised="2024-11-18"

# Compiler stage
FROM intel/oneapi-hpckit:2023.2.1-devel-ubuntu22.04 AS build

ENV MPI=/opt/intel/oneapi/mpi/2021.10.0/
ENV MOHIDPATH=/Mohid
ENV SRCPATH=/Mohid/Software

# Atualiza a lista de pacotes e instala ferramentas essenciais para compilação
RUN rm -rf /etc/apt/sources.list.d/* && \
    apt update && \
    apt install m4 autoconf automake gcc git -y && \
    git clone https://github.com/Mohid-Water-Modelling-System/Mohid.git && \
    cd Mohid && \
    git checkout b06e6f0288774aaf27aadb1fb87769ced72c5353 && \
    cp -r /Mohid/Solutions/dockers/externalSoftware/ /externalSoftware && \
    cp -r /Mohid/Software/ /src

# Define o shell padrão como Bash (pode ser necessário para scripts)
RUN ln -sf /bin/bash /bin/sh
# Caso seja necessário um link explícito para bash no caminho
# RUN ln -sf /bin/bash /usr/bin/bash

# Instala a biblioteca Zlib usando o script fornecido
RUN chmod +x /externalSoftware/install_zlib.sh && \
    ./externalSoftware/install_zlib.sh

# Instala a biblioteca HDF5 usando o script fornecido
RUN chmod +x /externalSoftware/install_hdf5.sh && \
    ./externalSoftware/install_hdf5.sh

# Instala a biblioteca NetCDF usando o script fornecido
RUN chmod +x /externalSoftware/install_nc.sh && \
    ./externalSoftware/install_nc.sh

# Define variáveis de ambiente para diretórios de instalação
ENV DIRINSTALL=/root/apps_intel
ENV zlib='zlib-1.2.11'
ENV hdf5='hdf5-1.8.17'
ENV netcdf='netcdf-4.4.1.1'
ENV netcdff='netcdf-fortran-4.4.4'


# Configura o ambiente para Zlib
ENV ZLIB=$DIRINSTALL/$zlib
ENV PATH=$PATH:$ZLIB/lib:$ZLIB/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ZLIB/lib

# Configura o ambiente para HDF5
ENV HDF5=$DIRINSTALL/$hdf5
ENV PATH=$PATH:$HDF5/bin:$HDF5/lib:$HDF5/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5/lib

# Configura o ambiente para NetCDF
ENV NETCDF=$DIRINSTALL/$netcdf
ENV PATH=$PATH:$NETCDF/bin:$NETCDF/lib:$NETCDF/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$NETCDF/lib

# Define o caminho do código-fonte no container
ENV SRCPATH=/src

# Prepara as dependências do Numerical Recipes usando o script fornecido
RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -mcmodel=large -xHost -ip -fpe3 -fpp -D_USE_MPI -D_NO_NETCDF -D_INCREASE_MAXINSTANCES_EXTRA -D_LAGRANGIAN_ -D_USE_NIX -D_STACK_LIMITS_ -D_BIG_LINE_LENGTH -D_INCREASE_MAXINSTANCES /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90 /Mohid/Software/MOHIDBase1/ModuleLUD.F90  /Mohid/Software/MOHIDBase1/ModuleTriangulation.F90  /Mohid/Software/MOHIDBase1/ModuleTime.F90  /Mohid/Software/MOHIDBase1/ModuleEnterData.F90  /Mohid/Software/MOHIDBase1/ModuleWWTPQ.F90  /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90  /Mohid/Software/MOHIDBase1/ModuleFunctions.F90  /Mohid/Software/MOHIDBase1/ModuleMacroAlgae.F90  /Mohid/Software/MOHIDBase1/ModuleWaterQuality.F90  /Mohid/Software/MOHIDBase1/ModuleSedimentQuality.F90  /Mohid/Software/MOHIDBase1/ModuleHydroIntegration.F90  /Mohid/Software/MOHIDBase1/ModuleSeagrassWaterInteraction.F90  /Mohid/Software/MOHIDBase1/ModuleHDF5.F90  /Mohid/Software/MOHIDBase1/ModuleHDF5_OO.F90  /Mohid/Software/MOHIDBase1/ModuleSeagrassSedimInteraction.F90  /Mohid/Software/MOHIDBase1/ModuleLife.F90  /Mohid/Software/MOHIDBase1/ModuleCEQUALW2.F90  /Mohid/Software/MOHIDBase1/ModuleBenthos.F90  /Mohid/Software/MOHIDBase1/ModuleDrawing.F90  /Mohid/Software/MOHIDBase1/ModuleProfile.F90  /Mohid/Software/MOHIDBase1/ModuleBivalve.F90  /Mohid/Software/MOHIDBase1/ModuleBenthicEcology.F90 /Mohid/Software/MOHIDBase1/ModuleInterface.F90  /Mohid/Software/MOHIDBase1/ModuleTimeSerie.F90  /Mohid/Software/MOHIDBase1/ModuleDischarges.F90  /Mohid/Software/MOHIDBase1/ModuleLightExtinction.F90  /Mohid/Software/MOHIDBase1/ModuleDrainageNetwork.F90  /Mohid/Software/MOHIDBase1/ModuleMPImanagement.F90  /Mohid/Software/MOHIDBase1/ModuleTask2000.F /Mohid/Software/MOHIDBase2/ModuleHorizontalGrid.F90  /Mohid/Software/MOHIDBase2/ModuleStatistic.F90  /Mohid/Software/MOHIDBase2/ModuleGridData.F90  /Mohid/Software/MOHIDBase2/ModuleBasinGeometry.F90  /Mohid/Software/MOHIDBase2/ModuleHorizontalMap.F90  /Mohid/Software/MOHIDBase2/ModuleBoxDif.F90  /Mohid/Software/MOHIDBase2/ModuleGeometry.F90  /Mohid/Software/MOHIDBase2/ModuleMap.F90  /Mohid/Software/MOHIDBase2/ModuleAdvectionDiffusion.F90  /Mohid/Software/MOHIDBase2/ModuleInterpolation.F90    /Mohid/Software/MOHIDBase2/ModuleTwoWay.F90  /Mohid/Software/MOHIDBase2/ModuleField4D.F90  /Mohid/Software/MOHIDBase2/ModuleFillMatrix.F90  /Mohid/Software/MOHIDBase2/ModuleChainReactions.F90  /Mohid/Software/MOHIDBase2/ModuleAtmosphere.F90 /Mohid/Software/MOHIDWater/ModuleTurbine.F90  /Mohid/Software/MOHIDWater/ModuleGOTM.F90  /Mohid/Software/MOHIDWater/ModuleTurbGOTM.F90  /Mohid/Software/MOHIDWater/ModuleFreeVerticalMovement.F90  /Mohid/Software/MOHIDWater/ModuleToga.F90  /Mohid/Software/MOHIDWater/ModuleGauge.F90  /Mohid/Software/MOHIDWater/ModuleOil.F90  /Mohid/Software/MOHIDWater/ModuleOil_0D.F90  /Mohid/Software/MOHIDWater/ModuleHNS.F90  /Mohid/Software/MOHIDWater/ModuleOpenBoundary.F90  /Mohid/Software/MOHIDWater/ModuleTurbulence.F90  /Mohid/Software/MOHIDWater/ModuleHydrodynamicFile.F90  /Mohid/Software/MOHIDWater/ModuleAssimilation.F90  /Mohid/Software/MOHIDWater/ModuleWaves.F90  /Mohid/Software/MOHIDWater/ModuleJet.F90  /Mohid/Software/MOHIDWater/ModuleSand.F90  /Mohid/Software/MOHIDWater/ModuleConsolidation.F90  /Mohid/Software/MOHIDWater/ModuleHydrodynamic.F90  /Mohid/Software/MOHIDWater/ModuleWaterProperties.F90 /Mohid/Software/MOHIDWater/ModuleSedimentProperties.F90  /Mohid/Software/MOHIDWater/ModuleSediment.F90  /Mohid/Software/MOHIDWater/ModuleInterfaceSedimentWater.F90  /Mohid/Software/MOHIDWater/ModuleInterfaceWaterAir.F90  /Mohid/Software/MOHIDWater/ModuleModel.F90 /Mohid/Software/MOHIDWater/Main.F90 -I$MPI/include -L$MPI/lib -lmpi -lmpifort -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -o MohidWater.exe

RUN cd /src && \
    ifort -O3 -qopenmp -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -mcmodel=large -xHost -ip -fpe3 -fpp -D_NO_NETCDF -D_INCREASE_MAXINSTANCES -D_BIG_LINE_LENGTH /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90  /Mohid/Software/MOHIDBase1/ModuleLUD.F90  /Mohid/Software/MOHIDBase1/ModuleTriangulation.F90 /Mohid/Software/MOHIDBase1/ModuleTime.F90 /Mohid/Software/MOHIDBase1/ModuleEnterData.F90 /Mohid/Software/MOHIDBase1/ModuleWWTPQ.F90 /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90 /Mohid/Software/MOHIDBase1/ModuleFunctions.F90 /Mohid/Software/MOHIDBase1/ModuleMacroAlgae.F90  /Mohid/Software/MOHIDBase1/ModuleWaterQuality.F90 /Mohid/Software/MOHIDBase1/ModuleSedimentQuality.F90 /Mohid/Software/MOHIDBase1/ModuleSeagrassWaterInteraction.F90 /Mohid/Software/MOHIDBase1/ModuleHDF5.F90 /Mohid/Software/MOHIDBase1/ModuleSeagrassSedimInteraction.F90 /Mohid/Software/MOHIDBase1/ModuleLife.F90 /Mohid/Software/MOHIDBase1/ModuleCEQUALW2.F90 /Mohid/Software/MOHIDBase1/ModuleBenthos.F90 /Mohid/Software/MOHIDBase1/ModuleDrawing.F90 /Mohid/Software/MOHIDBase1/ModuleProfile.F90 /Mohid/Software/MOHIDBase1/ModuleBivalve.F90 /Mohid/Software/MOHIDBase1/ModuleBenthicEcology.F90 /Mohid/Software/MOHIDBase1/ModuleInterface.F90 /Mohid/Software/MOHIDBase1/ModuleTimeSerie.F90  /Mohid/Software/MOHIDBase1/ModuleDischarges.F90 /Mohid/Software/MOHIDBase1/ModuleLightExtinction.F90 /Mohid/Software/MOHIDBase1/ModuleDrainageNetwork.F90 /Mohid/Software/MOHIDBase1/ModuleTask2000.F /Mohid/Software/MOHIDBase2/ModuleHorizontalGrid.F90 /Mohid/Software/MOHIDBase2/ModuleStatistic.F90  /Mohid/Software/MOHIDBase2/ModuleGridData.F90  /Mohid/Software/MOHIDBase2/ModuleBasinGeometry.F90 /Mohid/Software/MOHIDBase2/ModuleHorizontalMap.F90  /Mohid/Software/MOHIDBase2/ModuleBoxDif.F90 /Mohid/Software/MOHIDBase2/ModuleGeometry.F90 /Mohid/Software/MOHIDBase2/ModuleMap.F90 /Mohid/Software/MOHIDBase2/ModuleAdvectionDiffusion.F90 /Mohid/Software/MOHIDBase2/ModuleTwoWay.F90 /Mohid/Software/MOHIDBase2/ModuleField4D.F90   /Mohid/Software/MOHIDBase2/ModuleFillMatrix.F90 /Mohid/Software/MOHIDBase2/ModuleAtmosphere.F90 /Mohid/Software/MOHIDBase2/ModuleChainReactions.F90 /Mohid/Software/MOHIDLand/ModuleRunOff.F90 /Mohid/Software/MOHIDLand/ModuleRunoffProperties.F90 /Mohid/Software/MOHIDLand/ModulePorousMedia.F90 /Mohid/Software/MOHIDLand/ModulePorousMediaProperties.F90 /Mohid/Software/MOHIDLand/ModuleVegetation.F90 /Mohid/Software/MOHIDLand/ModuleSnow.F90 /Mohid/Software/MOHIDLand/ModuleIrrigation.F90 /Mohid/Software/MOHIDLand/ModuleReservoirs.F90 /Mohid/Software/MOHIDLand/ModuleBasin.F90 /Mohid/Software/MOHIDLand/MohidLand.F90 -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -o MohidLand.exe

RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -fp-model source -xHost -ip -fpe3 -fpp -D_INCREASE_MAXINSTANCES -D_NO_NETCDF  /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90 /Mohid/Software/MOHIDBase1/ModuleTime.F90 /Mohid/Software/MOHIDBase1/ModuleEnterData.F90  /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90 /Mohid/Software/MOHIDBase1/ModuleFunctions.F90 /Mohid/Software/MOHIDBase1/ModuleHDF5.F90 /Mohid/Software/DomainDecompositionConsolidation/ModuleHashTable.F90 /Mohid/Software/DomainDecompositionConsolidation/ModuleDDC.F90 /Mohid/Software/DomainDecompositionConsolidation/MohidDDC.F90 -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -o MohidDDC.exe

RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -fp-model source -xHost -ip -fpe3 -fpp -D_USE_NIX /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90 /Mohid/Software/MOHIDBase1/ModuleTime.F90 /Mohid/Software/MOHIDBase1/ModuleEnterData.F90 /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90 /Mohid/Software/MOHIDBase1/ModuleFunctions.F90 /Mohid/Software/MOHIDBase1/ModuleHDF5.F90 /Mohid/Software/MOHIDBase1/ModuleDrawing.F90 /Mohid/Software/MOHIDBase2/ModuleHorizontalGrid.F90 /Mohid/Software/MOHIDBase2/ModuleNETCDF.F90 /Mohid/Software/SmallTools/Convert2netcdf/Convert2netcdf.F90 -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -I$NETCDF/include -L$NETCDF/lib -lnetcdf -lnetcdff -o Convert2netcdf.exe

RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -fp-model source -xHost -ip -fpe3 -fpp -D_INCREASE_MAXINSTANCES_EXTRA -D_USE_NIX -D_STACK_LIMITS_ -D_BIG_LINE_LENGTH -D_INCREASE_MAXINSTANCES /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90 /Mohid/Software/MOHIDBase1/ModuleTriangulation.F90  /Mohid/Software/MOHIDBase1/ModuleTime.F90  /Mohid/Software/MOHIDBase1/ModuleEnterData.F90  /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90  /Mohid/Software/MOHIDBase1/ModuleFunctions.F90  /Mohid/Software/MOHIDBase1/ModuleHDF5.F90  /Mohid/Software/MOHIDBase1/ModuleDrawing.F90  /Mohid/Software/MOHIDBase1/ModuleTimeSerie.F90 /Mohid/Software/MOHIDBase1/ModuleDischarges.F90 /Mohid/Software/MOHIDBase1/ModuleTask2000.F  /Mohid/Software/MOHIDBase2/ModuleHorizontalGrid.F90  /Mohid/Software/MOHIDBase2/ModuleGridData.F90  /Mohid/Software/MOHIDBase2/ModuleBasinGeometry.F90  /Mohid/Software/MOHIDBase2/ModuleHorizontalMap.F90 /Mohid/Software/MOHIDBase2/ModuleBoxDif.F90  /Mohid/Software/MOHIDBase2/ModuleGeometry.F90  /Mohid/Software/MOHIDBase2/ModuleMap.F90  /Mohid/Software/MOHIDBase2/ModuleInterpolation.F90  /Mohid/Software/MOHIDBase2/ModuleTwoWay.F90 /Mohid/Software/MOHIDBase2/ModuleNETCDF.F90 /Mohid/Software/MOHIDBase2/ModuleField4D.F90 /Mohid/Software/MOHIDBase2/ModuleFillMatrix.F90 /Mohid/Software/ConvertToHDF5/ncdflib.F90 /Mohid/Software/ConvertToHDF5/ModuleAladinFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleARPSFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleARPSToWW3.F90 /Mohid/Software/ConvertToHDF5/ModuleCFFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleCFPolcomFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleCOWAMAAsciiWind.F90 /Mohid/Software/ConvertToHDF5/ModuleERA40Format.F90 /Mohid/Software/ConvertToHDF5/ModuleHYCOMFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleIHRadarFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleMERCATORFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleDelft3D_2_Mohid.F90 /Mohid/Software/ConvertToHDF5/ModuleMOG2DFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleReadSWANNonStationary.F90 /Mohid/Software/ConvertToHDF5/ModuleWOAFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleNetCDFCF_2_HDF5MOHID.F90 /Mohid/Software/ConvertToHDF5/ModuleEUCenterFormat.F90 /Mohid/Software/ConvertToHDF5/ModuleGFSasciiWind.F90 /Mohid/Software/ConvertToHDF5/ModuleGlueHDF5Files.F90 /Mohid/Software/ConvertToHDF5/ModuleHDF5ToASCIIandBIN.F90 /Mohid/Software/ConvertToHDF5/ModuleHellermanRosensteinAscii.F90 /Mohid/Software/ConvertToHDF5/ModuleInterpolateGrids.F90 /Mohid/Software/ConvertToHDF5/ModuleInterpolateTime.F90 /Mohid/Software/ConvertToHDF5/ModuleLevitusFormat.F90     /Mohid/Software/ConvertToHDF5/ModuleMM5Format.F90 /Mohid/Software/ConvertToHDF5/ModulePatchHDF5Files.F90 /Mohid/Software/ConvertToHDF5/ModuleSWAN.F90 /Mohid/Software/ConvertToHDF5/ModuleTecnoceanAscii.F90 /Mohid/Software/ConvertToHDF5/ModuleUpscaleHDF5.F90 /Mohid/Software/ConvertToHDF5/ConvertToHDF5.F90 -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -I$NETCDF/include -L$NETCDF/lib -lnetcdf -lnetcdff -o ConvertToHDF5.exe

RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -fp-model source -xHost -ip -fpe3 -fpp -D_BIG_LINE_LENGTH /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90 /Mohid/Software/MOHIDBase1/ModuleTime.F90 /Mohid/Software/MOHIDBase1/ModuleEnterData.F90 /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90 /Mohid/Software/MOHIDBase1/ModuleFunctions.F90 /Mohid/Software/MOHIDBase1/ModuleHDF5.F90 /Mohid/Software/MOHIDBase1/ModuleDrawing.F90 /Mohid/Software/MOHIDBase1/ModuleTimeSerie.F90 /Mohid/Software/MOHIDBase2/ModuleHorizontalGrid.F90 /Mohid/Software/MOHIDBase2/ModuleGridData.F90  /Mohid/Software/HDF5Exporter/ModuleExportHDF5ToTimeSerie.F90	/Mohid/Software/HDF5Exporter/HDF5Exporter.F90 -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -o HDF5Exporter.exe

RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -fp-model source -xHost -ip -fpe3 -fpp -D_NO_NETCDF /Mohid/Software/MOHIDBase1/ModuleGlobalData.F90 /Mohid/Software/MOHIDBase1/ModuleTime.F90 /Mohid/Software/MOHIDBase1/ModuleEnterData.F90 /Mohid/Software/MOHIDBase1/ModuleStopWatch.F90 /Mohid/Software/MOHIDBase1/ModuleFunctions.F90 /Mohid/Software/MOHIDBase1/ModuleHDF5.F90 /Mohid/Software/MOHIDBase1/ModuleDrawing.F90 /Mohid/Software/HDF5Extractor/ModuleHDF5Extractor.F90 /Mohid/Software/HDF5Extractor/HDF5Extractor.F90 -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -o HDF5Extractor.exe

## Final Stage: Prepare the MOHID application environment
# FROM base AS final

# COPY --from=build /opt/intel/oneapi/mpi/2021.10.0/ /opt/intel/oneapi/mpi/2021.10.0/

# COPY --from=build /lib64/ld-linux-x86-64.so.2 /lib64/ld-linux-x86-64.so.2
# COPY --from=build /lib/x86_64-linux-gnu/libm.so.6 /lib/x86_64-linux-gnu/libm.so.6
# COPY --from=build /lib/x86_64-linux-gnu/libc.so.6 /lib/x86_64-linux-gnu/libc.so.6
# COPY --from=build /lib/x86_64-linux-gnu/librt.so.1 /lib/x86_64-linux-gnu/librt.so.1
# COPY --from=build /lib/x86_64-linux-gnu/libdl.so.2 /lib/x86_64-linux-gnu/libdl.so.2
# COPY --from=build /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/x86_64-linux-gnu/libgcc_s.so.1
# COPY --from=build /lib/x86_64-linux-gnu/libpthread.so.0 /lib/x86_64-linux-gnu/libpthread.so.0
# COPY --from=build /root/apps_intel/zlib-1.2.11/lib/libz.so.1 /root/apps_intel/zlib-1.2.11/lib/libz.so.1
# COPY --from=build /root/apps_intel/hdf5-1.8.17/lib/libhdf5.so.10 /root/apps_intel/hdf5-1.8.17/lib/libhdf5.so.10
# COPY --from=build /root/apps_intel/hdf5-1.8.17/lib/libhdf5_hl.so.10 /root/apps_intel/hdf5-1.8.17/lib/libhdf5_hl.so.10
# COPY --from=build /root/apps_intel/netcdf-4.4.1.1/lib/libnetcdf.so.11 /root/apps_intel/netcdf-4.4.1.1/lib/libnetcdf.so.11
# COPY --from=build /root/apps_intel/netcdf-4.4.1.1/lib/libnetcdff.so.6 /root/apps_intel/netcdf-4.4.1.1/lib/libnetcdff.so.6
# COPY --from=build /opt/intel/oneapi/mpi/2021.10.0//lib/libmpifort.so.12 /opt/intel/oneapi/mpi/2021.10.0//lib/libmpifort.so.12
# COPY --from=build /root/apps_intel/hdf5-1.8.17/lib/libhdf5_fortran.so.10 /root/apps_intel/hdf5-1.8.17/lib/libhdf5_fortran.so.10
# COPY --from=build /root/apps_intel/hdf5-1.8.17/lib/libhdf5hl_fortran.so.10 /root/apps_intel/hdf5-1.8.17/lib/libhdf5hl_fortran.so.10
# COPY --from=build /opt/intel/oneapi/mpi/2021.10.0//lib/release/libmpi.so.12 /opt/intel/oneapi/mpi/2021.10.0//lib/release/libmpi.so.12
# COPY --from=build /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libimf.so /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libimf.so
# COPY --from=build /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libsvml.so /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libsvml.so
# COPY --from=build /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libiomp5.so /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libiomp5.so
# COPY --from=build /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libintlc.so.5 /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libintlc.so.5
# COPY --from=build /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libifport.so.5 /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libifport.so.5
# COPY --from=build /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libifcoremt.so.5 /opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin/libifcoremt.so.5


# COPY --from=build /src/MohidWater.exe /usr/local/bin/MohidWater.exe
# COPY --from=build /src/MohidLand.exe /usr/local/bin/MohidLand.exe
# COPY --from=build /src/MohidDDC.exe /usr/local/bin/MohidDDC.exe
# COPY --from=build /src/Convert2netcdf.exe /usr/local/bin/Convert2netcdf.exe
# COPY --from=build /src/ConvertToHDF5.exe /usr/local/bin/ConvertToHDF5.exe
# COPY --from=build /src/HDF5Exporter.exe /usr/local/bin/HDF5Exporter.exe
# COPY --from=build /src/HDF5Extractor.exe /usr/local/bin/HDF5Extractor.exe

# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/lib64:/lib/x86_64-linux-gnu:/root/apps_intel/zlib-1.2.11/lib:/root/apps_intel/hdf5-1.8.17/lib:/root/apps_intel/netcdf-4.4.1.1/lib:/opt/intel/oneapi/mpi/2021.10.0//lib:/opt/intel/oneapi/mpi/2021.10.0//lib/release:/opt/intel/oneapi/compiler/2023.2.1/linux/compiler/lib/intel64_lin
# ENV PATH=$PATH:/opt/intel/oneapi/mpi/2021.10.0/bin