#!/bin/bash

cd /home/amr-wind-input-example

mpirun --allow-run-as-root --use-hwthread-cpus -np 2 amr_wind abl_amd_wenoz.inp