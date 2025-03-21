#!/bin/bash

cd /home/reef3d-input-example

# Change the number of processors to 1
sed -i 's/M 10 4/M 10 1/g' control.txt
sed -i 's/M 10 4/M 10 1/g' ctrl.txt

/DIVEMesh/bin/DiveMESH
/REEF3D/bin/REEF3D
