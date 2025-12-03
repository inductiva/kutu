#!/bin/bash
set -e

# Install dependencies
apt-get update && apt-get install -y --no-install-recommends curl unzip ca-certificates

echo "=========================================="
echo "TEST 1: Basic D-Flow FM simulation"
echo "=========================================="

# Download and unzip D-Flow FM example
curl -L -o /tmp/delft3dfm-input-example.zip https://storage.googleapis.com/inductiva-api-demo-files/delft3dfm-input-example.zip
unzip -q /tmp/delft3dfm-input-example.zip -d /tmp

cd /tmp/delft3dfm-input-example
dflowfm --autostartstop f34.mdu

echo ""
echo "=========================================="
echo "TEST 2: D-Flow FM with WAQ processes (via DIMR)"
echo "=========================================="

# Copy example to temp (to avoid writing to read-only image location)
cp -r /home/examples/dflowfm_dwaq /tmp/dflowfm_dwaq
cd /tmp/dflowfm_dwaq

echo "Running D-Flow FM with inline water quality processes..."
dimr dimr_config.xml

echo ""
echo "=========================================="
echo "TEST 3: Standalone D-WAQ (delwaq)"
echo "=========================================="

cp -r /home/examples/delwaq_standalone /tmp/delwaq_standalone
cd /tmp/delwaq_standalone

echo "Running standalone D-WAQ water quality simulation..."
delwaq com-tut_fti_waq.inp -p $PROC_DEF_DIR/proc_def.dat

echo ""
echo "=========================================="
echo "TEST 4: D-Flow FM + D-Waves (coupled)"
echo "=========================================="

cp -r /home/examples/dflowfm_dwaves /tmp/dflowfm_dwaves
cd /tmp/dflowfm_dwaves

echo "Running D-Flow FM coupled with D-Waves..."
dimr dimr_config.xml

echo ""
echo "=========================================="
echo "All tests completed successfully!"
echo "=========================================="
