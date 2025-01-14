#!/bin/bash

# Set the working directory
WORKDIR="/opt/COAWST/Lib/SCRIP_COAWST"

# Define the input file (relative to WORKDIR)
INPUT_FILE="scrip_coawst_inlet_test_refined.in"

# Change to the working directory
echo "Changing to working directory: $WORKDIR"
cd $WORKDIR || { echo "Error: Failed to change to directory $WORKDIR"; exit 1; }

# Check if the input file exists in the working directory
if [[ ! -f $INPUT_FILE ]]; then
  echo "Error: Input file '$INPUT_FILE' not found in $WORKDIR."
  exit 1
fi

# Run the simulation
echo "Running scrip_coawst with input file: $INPUT_FILE"
./scrip_coawst $INPUT_FILE 

# Check if the simulation ran successfully
if [[ $? -eq 0 ]]; then
  echo "Simulation completed successfully."
else
  echo "Simulation failed. Check simulation.log for details."
  exit 1
fi
