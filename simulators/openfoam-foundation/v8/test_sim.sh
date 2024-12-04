#!/bin/bash

cd /home/openfoam-input-example

surfaceFeatures
blockMesh && \
decomposePar -copyZero && \
snappyHexMesh -overwrite && \
potentialFoam && \
simpleFoam
