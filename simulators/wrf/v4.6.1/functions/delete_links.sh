#!/bin/bash

# Find and delete all symbolic links in the current directory
find . -maxdepth 1 -type l -exec rm -v {} \;
