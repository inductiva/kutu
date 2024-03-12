#!/bin/bash

# Set up symbolic links to the executables in the bin directory
# so that they can be called with more convenient names (e.g., partvk
# instead of PartVTK_linux64)
DUALSPHYSICS_BIN_DIR="/DualSPHysics_v5.2/bin/linux"

for file_path in $DUALSPHYSICS_BIN_DIR/*; do
    echo "Setting up $file_path..."

    # Remove _linux64 suffix and convert to lowercase
    new_file_name=$(basename ${file_path%_linux64} | tr '[:upper:]' '[:lower:]')
    echo "New file name: $new_file_name"

    new_file_path=$(dirname $file_path)/$new_file_name
    if [ ! -f $new_file_path ]; then
        ln -s $file_path $new_file_path
        chmod +x $new_file_path
        echo "Symbolic link to $file_path in $new_file_path set up."
    fi
done

