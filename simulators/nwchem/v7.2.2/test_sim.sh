#!/bin/bash

cd /home/nwchem-input-example

mpirun --allow-run-as-root --np 4 --use-hwthread-cpus nwchem h2o_sp_scf.nw