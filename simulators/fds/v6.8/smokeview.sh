#!/bin/bash

Xvfb :1 -screen 0 1024x768x16 &
/opt/smokeview/smvbin/smokeview -runscript $1

# Terminate Xvfb
kill -s SIGTERM $!
