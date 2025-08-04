#!/bin/bash
# Usage: bash script.sh Ifremer2 [true|false]

# if the second argument is true we consider the switch to be a custom switch
# provided by the user, and will copy it to the model/bin dir
# otherwise we assume it is a switch provided by ww3 and should already be there

# Exit on any error
set -e

echo "[DEBUG] Current working directory before script starts:"
pwd

echo "[DEBUG] Copying /WW3 to __WW3..."
cp -r /WW3 __WW3

echo "[DEBUG] Changing directory to __WW3..."
cd __WW3
pwd

export WW3=/workdir/output/artifacts/__WW3
echo "[DEBUG] WW3 environment variable set to: $WW3"

# Check if argument is provided
if [ -z "$1" ]; then
  echo "Usage: bash $0 <SWITCH_NAME>"
  exit 1
fi

SWITCH_NAME=$1
echo "[DEBUG] SWITCH_NAME set to: $SWITCH_NAME"
IS_CUSTOM="$2"

# If IS_CUSTOM is set to "true" (case-insensitive), copy the switch file
if [[ "${IS_CUSTOM,,}" == "true" ]]; then
  echo "[DEBUG] IS_CUSTOM is true, copying custom switch..."
  BASENAME=$(basename "$SWITCH_NAME")
  cp -f "/workdir/output/artifacts/$SWITCH_NAME" "model/bin/switch_${BASENAME}"
  echo "[DEBUG] Copied $SWITCH_NAME to model/bin/switch_${BASENAME}"
fi

echo "[DEBUG] Removing any existing build directory..."
rm -rf build
echo "[DEBUG] Creating build directory..."
mkdir -p build

echo "[DEBUG] Changing into build directory..."
cd build
pwd

echo "[DEBUG] Running cmake with source directory /workdir/output/artifacts/__WW3"
cmake /workdir/output/artifacts/__WW3 -DSWITCH=${SWITCH_NAME} \
  -DNetCDF_INCLUDE_DIRS=/WW3_LIBRARIES/include \
  -DNetCDF_LIBRARIES="/WW3_LIBRARIES/lib/libnetcdf.so;/WW3_LIBRARIES/lib/libnetcdff.so" \
  -DNetCDF_C_LIBRARY=/WW3_LIBRARIES/lib/libnetcdf.so \
  -DNetCDF_F90_LIBRARY=/WW3_LIBRARIES/lib/libnetcdff.so

echo "[DEBUG] Running make -j"
make -j

echo "[DEBUG] Build finished. Returning to artifacts directory..."
cd ../..
pwd
