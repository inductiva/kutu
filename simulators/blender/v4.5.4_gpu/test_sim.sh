#!/bin/bash

# Test Blender installation by checking version
blender --version

# Run Blender in headless mode with a simple Python script to verify it works
blender --background --python-expr "import bpy; print('Blender GPU image is working correctly')"
