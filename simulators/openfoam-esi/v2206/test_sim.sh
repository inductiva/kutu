#!/bin/bash

cd /home/openfoam-esi-input-example

surfaceFeatureExtract && \
blockMesh && \
decomposePar -copyZero && \
cp -r 0.orig/ 0 && \
snappyHexMesh -overwrite && \
potentialFoam && \
simpleFoam
