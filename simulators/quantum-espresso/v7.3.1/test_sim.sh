#!/bin/bash

cd /home/qe-input-example

#Serial run with mpi binary
pw.x -i Al_local_pseudo.in
pw.x -i Al_qe_pseudo.in

#Mpi run
mpirun --allow-run-as-root -np 4 pw.x -i Al_local_pseudo.in
mpirun --allow-run-as-root -np 4 pw.x -i Al_qe_pseudo.in

#Openmp binary
pw_openmp.x -i Al_local_pseudo.in
pw_openmp.x -i Al_qe_pseudo.in