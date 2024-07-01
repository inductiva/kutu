#!/bin/bash

cd /home/swash-input-example
mv input.sws INPUT

mpirun --allow-run-as-root -np 4 swash.exe
