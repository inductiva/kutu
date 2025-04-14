#!/bin/bash

cd /home/dualsphysics-input-example

/DualSPHysics/bin/linux/gencase config flow_cylinder -save:all && \
/DualSPHysics/bin/linux/dualsphysics5.4cpu flow_cylinder flow_cylinder -dirdataout data -svres && \
/DualSPHysics/bin/linux/partvtk -dirin flow_cylinder/data -savevtk flow_cylinder/PartFluid -onlytype:-all,+fluid
