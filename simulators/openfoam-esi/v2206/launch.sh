#!/bin/bash

# Utility to run OpenFOAM commands that sources the OpenFOAM startup file
source $OPENFOAM_SOURCE_FILE

# Run the command
$1
