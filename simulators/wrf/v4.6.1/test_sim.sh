#!/bin/bash

cd /home/wrf-input-example

/scripts/create_links.sh /WRF/test/em_fire

./ideal.exe

mpirun --allow-run-as-root -np 2 ./wrf.exe