#!/bin/bash

cd /home/nwchem-input-example

mpirun --allow-run-as-root --np 4 --use-hwthread-cpus nwchem 5h2o_core.nw