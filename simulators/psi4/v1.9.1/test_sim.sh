#!/bin/bash
cd /opt/psi4build/psi4/objdir
make pytest
cd /home
mpirun -np 4 --allow-run-as-root psi4 example.in