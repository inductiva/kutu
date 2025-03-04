#!/bin/bash
set -euo pipefail

jupyter lab --ip=0.0.0.0 --port=53155 --no-browser --allow-root
# mpiexec -np 2 /home/tools/bin/SeisSol_Release_dhsw_4_elastic /home/seissol/examples/tpv33/parameters.par


