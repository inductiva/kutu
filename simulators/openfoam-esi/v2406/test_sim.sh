#!/bin/bash

cd /home/openfoam-esi-input-example

/launch.sh "surfaceFeatureExtract" && \
/launch.sh "blockMesh" && \
/launch.sh "decomposePar -copyZero" && \
cp -r 0.orig/ 0 && \
/launch.sh "snappyHexMesh -overwrite" && \
/launch.sh "potentialFoam" && \
/launch.sh "simpleFoam"
