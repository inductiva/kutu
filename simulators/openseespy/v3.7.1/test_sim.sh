#!/bin/bash

python Example1.1.py
python Example2.1.py
python Example3.1.py
python Example3.2.py
python Example3.3.py
python Example4.1.py
python Example5.1.py
python Example6.1.py
python Example7.1.py
python Example8.1.py
mpirun -np 2 --allow-run-as-root python example_mpi_paralleltruss_explicit.py