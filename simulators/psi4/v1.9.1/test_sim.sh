#!/bin/bash
cd /home
mpirun -np 4 --allow-run-as-root psi4 example.in output.in
cat output.in