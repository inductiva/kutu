#!/bin/bash

cd /home/swash-input-example
mv input.sws INPUT

mpirun --allow-run-as-root --use-hwthread-cpus -np 2 swash.exe
