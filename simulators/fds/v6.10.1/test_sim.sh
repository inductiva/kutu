#!/bin/bash

cd /home/fds-input-example

fds mccaffrey.fds

# Since fds returns 0 even if the simulation fails, we need to check the output 
# file to know if the simulation was successful.
grep -q "FDS completed successfully" mccaffrey.out 