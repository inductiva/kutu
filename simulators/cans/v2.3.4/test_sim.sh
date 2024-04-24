#!/bin/bash
cd /home/cans-input-example

mpirun --allow-run-as-root --np 4 --use-hwthread-cpus cans
