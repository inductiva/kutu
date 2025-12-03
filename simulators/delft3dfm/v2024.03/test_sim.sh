#!/bin/bash
set -e

# Install dependencies
apt-get update && apt-get install -y --no-install-recommends curl unzip subversion ca-certificates

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
echo "TEST 2: D-Flow FM + D-WAQ (Water Quality)"
echo "=========================================="

# Download D-WAQ example from Deltares SVN
# Source: https://svn.oss.deltares.nl/repos/delft3d/tags/delft3dfm/142431/examples/
svn export --quiet https://svn.oss.deltares.nl/repos/delft3d/trunk/examples/dflowfm/03_dflowfm_dwaq_sequential /tmp/dwaq_example || {
    echo "Could not download D-WAQ example from SVN, skipping..."
    echo "All available tests completed!"
    exit 0
}

cd /tmp/dwaq_example/dflowfm
echo "Running D-Flow FM with Water Quality (D-WAQ)..."
dflowfm --autostartstop f34_dynamo.mdu

echo ""
echo "=========================================="
echo "All tests completed successfully!"
echo "=========================================="
