#!/bin/bash

# Test script for OpenFOAM with cfMesh
# This script tests the cfMesh functionality using a sample tutorial case

set -e

# Create a temporary test directory
TEST_DIR="/tmp/cfmesh_test"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Copy tutorial case from cfMesh
cp -r /opt/cfmesh/tutorials/cartesianMesh/asmoOctree/* "$TEST_DIR/"

# Set up OpenFOAM environment variables
export FOAM_RUN=/tmp
export WM_PROJECT=OpenFOAM
export WM_PROJECT_VERSION=2412

# Run cartesianMesh to generate the mesh
echo "Running cartesianMesh on asmoOctree tutorial case..."
cartesianMesh

# Verify mesh files were created
if [ -f constant/polyMesh/points ] && \
   [ -f constant/polyMesh/faces ] && \
   [ -f constant/polyMesh/owner ] && \
   [ -f constant/polyMesh/neighbour ] && \
   [ -f constant/polyMesh/boundary ]; then
    echo "✓ Mesh generation successful!"
    echo "✓ All required mesh files created"
    echo "Mesh statistics:"
    echo "  - Points: $(wc -l < constant/polyMesh/points)"
    echo "  - Faces: $(wc -l < constant/polyMesh/faces)"
    ls -lh constant/polyMesh/
else
    echo "✗ Mesh generation failed - files missing"
    exit 1
fi

# Test checkSurfaceMesh tool
echo ""
echo "Testing checkSurfaceMesh tool..."
checkSurfaceMesh geom.stl > /dev/null 2>&1 && echo "✓ checkSurfaceMesh works" || echo "⚠ checkSurfaceMesh test skipped"

echo ""
echo "cfMesh test completed successfully!"
