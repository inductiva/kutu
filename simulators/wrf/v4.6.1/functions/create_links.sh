#!/bin/sh

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

INPUT_FOLDER="$1"

# Check if the input is a directory
if [ ! -d "$INPUT_FOLDER" ]; then
  echo "Error: '$INPUT_FOLDER' is not a directory"
  exit 1
fi

# Loop over the contents of the input folder
for item in "$INPUT_FOLDER"/*; do
  # Skip if no files match (i.e., folder is empty)
  [ -e "$item" ] || continue

  base=$(basename "$item")

  if [ ! -e "$base" ]; then
    ln -snf "$item" "$base"
    echo "Created symlink for $base"
  else
    echo "File $base already exists, skipping."
  fi
done
