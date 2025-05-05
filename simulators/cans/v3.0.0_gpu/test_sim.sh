#!/bin/bash
cd /home/cansv3.0.0-input-example

mpirun --allow-run-as-root --np 4 --use-hwthread-cpus cans
