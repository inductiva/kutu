#!/bin/bash
# Usage: bash script.sh Ifremer2
# Should be called inside the WW3 dir

# Exit on any error
set -e

# Check if argument is provided
if [ -z "$1" ]; then
  echo "Usage: bash $0 <SWITCH_NAME>"
  exit 1
fi

SWITCH_NAME=$1
mkdir -p build
cd build

cmake .. -DSWITCH=${SWITCH_NAME} \
  -DNetCDF_INCLUDE_DIRS=/WW3_LIBRARIES/include \
  -DNetCDF_LIBRARIES="/WW3_LIBRARIES/lib/libnetcdf.so;/WW3_LIBRARIES/lib/libnetcdff.so" \
  -DNetCDF_C_LIBRARY=/WW3_LIBRARIES/lib/libnetcdf.so \
  -DNetCDF_F90_LIBRARY=/WW3_LIBRARIES/lib/libnetcdff.so

make -j
