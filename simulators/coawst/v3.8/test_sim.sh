#!/bin/bash

cd /opt/COAWST

mpirun --allow-run-as-root --use-hwthread-cpus -np 2 coawstM Projects/Inlet_test/Refined/coupling_inlet_test_ref3.in
