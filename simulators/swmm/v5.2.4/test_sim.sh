#!/bin/bash
set -euo pipefail

runswmm --version
runswmm --help | head -n 5

# Test Example8 from EPA SWMM5 Applications Manual
echo "Downloading EPA SWMM5 Applications Manual..."
curl -L -o epaswmm5_apps_manual.zip "https://www.epa.gov/sites/default/files/2014-05/epaswmm5_apps_manual.zip"
unzip -q epaswmm5_apps_manual.zip
unzip -q epaswmm5_apps_manual/files.zip -d epaswmm5_apps_manual/

echo "Testing Example9..."
runswmm epaswmm5_apps_manual/Example9.inp epaswmm5_apps_manual/Example9.rpt
echo "Example9 test completed successfully"

# Cleanup
rm -rf epaswmm5_apps_manual.zip epaswmm5_apps_manual __MACOSX
