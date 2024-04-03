#!/bin/bash

cd /home/openfoam-input-example

/launch.sh "surfaceFeatures" && \
/launch.sh "blockMesh" && \
/launch.sh "decomposePar -copyZero" && \
/launch.sh "snappyHexMesh -overwrite" && \
/launch.sh "potentialFoam" && \
/launch.sh "simpleFoam"
