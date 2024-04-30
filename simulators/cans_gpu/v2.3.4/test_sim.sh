#!/bin/bash
cd /home/cans-input-example

mpirun --allow-run-as-root --np 1 --use-hwthread-cpus cans
