#!/bin/bash

gmx solvate -cs tip4p -box 2.3 -o conf.gro -p /home/gromacs-input-example/topol.top
