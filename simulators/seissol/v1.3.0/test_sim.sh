#!/bin/bash
set -euo pipefail

jupyter lab --ip=0.0.0.0 --port=53155 --no-browser --allow-root
# mpirun --allow-run-as-root --oversubscribe --use-hwthread-cpus -np 2 SeisSol_Release_dhsw_4_elastic /home/seissol/examples/tpv33/parameters.par
#mpiexec -np 2 /home/tools/bin/SeisSol_Release_dhsw_4_elastic /home/seissol/examples/tpv33/parameters.par