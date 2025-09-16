#!/bin/bash

cd /home/funwave-input-example

mpirun --allow-run-as-root --use-hwthread-cpus -np 4 /FUNWAVE-TVD-Version_3.6/funwave-work/funwave--mpif90-parallel-single input.txt