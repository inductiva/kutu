#!/bin/bash

# Utility to run OpenFOAM commands that sources the OpenFOAM startup file
source $OPENFOAM_SOURCE_FILE

# RUN the command
$1
