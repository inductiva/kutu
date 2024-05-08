#!/bin/bash

cd /home/schism-input-example
mkdir outputs

/schism/build/bin/pschism && \

# Check if the simulation ran successfully
# Schism can return 0 if an error occurs, so we need to check the output
grep "********CG Solve at timestep     2880" outputs/JCG.out
