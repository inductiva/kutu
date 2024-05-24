#!/usr/bin/env bash

echo $(date)

echo "Running echo with the following arguments:"

for arg in "$@"
do
    echo " - $arg"
done
echo "All done"
