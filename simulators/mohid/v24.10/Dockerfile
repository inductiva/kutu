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

# Define variáveis de ambiente para diretórios de instalação
ENV DIRINSTALL=/root/apps_intel
ENV zlib='zlib-1.2.11'
ENV hdf5='hdf5-1.8.17'

# Configura o ambiente para Zlib
ENV ZLIB=$DIRINSTALL/$zlib
ENV PATH=$PATH:$ZLIB/lib:$ZLIB/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ZLIB/lib

# Configura o ambiente para HDF5
ENV HDF5=$DIRINSTALL/$hdf5
ENV PATH=$PATH:$HDF5/bin:$HDF5/lib:$HDF5/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5/lib

# Define o caminho do código-fonte no container
ENV SRCPATH=/src

# Prepara as dependências do Numerical Recipes usando o script fornecido
RUN cd /src && \
    ifort -O3 -w -cpp -real-size 64 -convert little_endian -fPIC -heap-arrays 64 -mcmodel=large -xHost -ip -fpe3 -fpp -D_USE_MPI -D_NO_NETCDF -D_INCREASE_MAXINSTANCES_EXTRA -D_LAGRANGIAN_ -D_USE_NIX -D_STACK_LIMITS_ -D_BIG_LINE_LENGTH -D_INCREASE_MAXINSTANCES $MohidBase1/ModuleGlobalData.F90 $MohidBase1/ModuleLUD.F90  $MohidBase1/ModuleTriangulation.F90  $MohidBase1/ModuleTime.F90  $MohidBase1/ModuleEnterData.F90  $MohidBase1/ModuleWWTPQ.F90  $MohidBase1/ModuleStopWatch.F90  $MohidBase1/ModuleFunctions.F90  $MohidBase1/ModuleMacroAlgae.F90  $MohidBase1/ModuleWaterQuality.F90  $MohidBase1/ModuleSedimentQuality.F90  $MohidBase1/ModuleHydroIntegration.F90  $MohidBase1/ModuleSeagrassWaterInteraction.F90  $MohidBase1/ModuleHDF5.F90  $MohidBase1/ModuleHDF5_OO.F90  $MohidBase1/ModuleSeagrassSedimInteraction.F90  $MohidBase1/ModuleLife.F90  $MohidBase1/ModuleCEQUALW2.F90  $MohidBase1/ModuleBenthos.F90  $MohidBase1/ModuleDrawing.F90  $MohidBase1/ModuleProfile.F90  $MohidBase1/ModuleBivalve.F90  $MohidBase1/ModuleBenthicEcology.F90 $MohidBase1/ModuleInterface.F90  $MohidBase1/ModuleTimeSerie.F90  $MohidBase1/ModuleDischarges.F90  $MohidBase1/ModuleLightExtinction.F90  $MohidBase1/ModuleDrainageNetwork.F90  $MohidBase1/ModuleMPImanagement.F90  $MohidBase1/ModuleTask2000.F $MohidBase2/ModuleHorizontalGrid.F90  $MohidBase2/ModuleStatistic.F90  $MohidBase2/ModuleGridData.F90  $MohidBase2/ModuleBasinGeometry.F90  $MohidBase2/ModuleHorizontalMap.F90  $MohidBase2/ModuleBoxDif.F90  $MohidBase2/ModuleGeometry.F90  $MohidBase2/ModuleMap.F90  $MohidBase2/ModuleAdvectionDiffusion.F90  $MohidBase2/ModuleInterpolation.F90    $MohidBase2/ModuleTwoWay.F90  $MohidBase2/ModuleField4D.F90  $MohidBase2/ModuleFillMatrix.F90  $MohidBase2/ModuleChainReactions.F90  $MohidBase2/ModuleAtmosphere.F90 $MohidWater/ModuleTurbine.F90  $MohidWater/ModuleGOTM.F90  $MohidWater/ModuleTurbGOTM.F90  $MohidWater/ModuleFreeVerticalMovement.F90  $MohidWater/ModuleToga.F90  $MohidWater/ModuleGauge.F90  $MohidWater/ModuleOil.F90  $MohidWater/ModuleOil_0D.F90  $MohidWater/ModuleHNS.F90  $MohidWater/ModuleOpenBoundary.F90  $MohidWater/ModuleTurbulence.F90  $MohidWater/ModuleHydrodynamicFile.F90  $MohidWater/ModuleAssimilation.F90  $MohidWater/ModuleWaves.F90  $MohidWater/ModuleJet.F90  $MohidWater/ModuleSand.F90  $MohidWater/ModuleConsolidation.F90  $MohidWater/ModuleHydrodynamic.F90  $MohidWater/ModuleWaterProperties.F90 $MohidWater/ModuleSedimentProperties.F90  $MohidWater/ModuleSediment.F90  $MohidWater/ModuleInterfaceSedimentWater.F90  $MohidWater/ModuleInterfaceWaterAir.F90  $MohidWater/ModuleModel.F90 $MohidWater/Main.F90 -I$MPI/include -L$MPI/lib -lmpi -lmpifort -I$HDF5/include -L$HDF5/lib -lhdf5hl_fortran -lhdf5_hl -lhdf5_fortran -lhdf5 -ldl -I$ZLIB/include -L$ZLIB/lib -lz -lm -o MohidWater.exe

## Final Stage: Prepare the MOHID application environment
FROM base AS final

# Cria o diretório principal para os binários e bibliotecas do MOHID
RUN mkdir /mohid

# Copia o executável compilado do MOHID da etapa de build
COPY --from=build /src/MohidWater.exe /mohid/MohidWater.exe

COPY --from=build /root/apps_intel /mohid_libs 

# Copia as bibliotecas compiladas (zlib, hdf5, etc.) da etapa de build para o diretório do container
COPY --from=build /root/apps_intel /mohid_libs 

# Cria um subdiretório para as bibliotecas Intel necessárias
RUN mkdir /mohid_libs/intel

# Copia as bibliotecas Intel necessárias do ambiente de build para o container
COPY --from=build /opt/intel/oneapi/compiler/latest/linux/compiler/lib/intel64_lin/libimf.so /mohid_libs/intel/libimf.so
COPY --from=build /opt/intel/oneapi/compiler/latest/linux/compiler/lib/intel64_lin/libsvml.so /mohid_libs/intel/libsvml.so
COPY --from=build /opt/intel/oneapi/compiler/latest/linux/compiler/lib/intel64_lin/libirng.so /mohid_libs/intel/libirng.so
COPY --from=build /opt/intel/oneapi/compiler/latest/linux/compiler/lib/intel64_lin/libintlc.so.5 /mohid_libs/intel/libintlc.so.5
COPY --from=build /opt/intel/oneapi/compiler/latest/linux/compiler/lib/intel64_lin/libifport.so.5 /mohid_libs/intel/libifport.so.5
COPY --from=build /opt/intel/oneapi/compiler/latest/linux/compiler/lib/intel64_lin/libifcoremt.so.5 /mohid_libs/intel/libifcoremt.so.5

# Adiciona os caminhos das bibliotecas ao sistema de bibliotecas compartilhadas
RUN echo "/mohid_libs/intel" >> /etc/ld.so.conf
RUN echo "/mohid_libs/mpich-3.2/lib" >> /etc/ld.so.conf
RUN echo "/mohid_libs/proj-4.9.3/lib" >> /etc/ld.so.conf
RUN echo "/mohid_libs/netcdf-4.4.1.1/lib" >> /etc/ld.so.conf
RUN echo "/mohid_libs/hdf5-1.8.17/lib" >> /etc/ld.so.conf
RUN echo "/mohid_libs/zlib-1.2.11/lib" >> /etc/ld.so.conf

COPY test_sim.sh /home/test_sim.sh
RUN chmod +x /home/test_sim.sh

# Atualiza o cache de bibliotecas compartilhadas para incluir os novos caminhos
RUN ldconfig