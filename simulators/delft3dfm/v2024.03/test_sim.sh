#!/bin/bash

# Download D-Flow FM example from Deltares SVN
apt-get update && apt-get install -y subversion
svn export --trust-server-cert-failures=unknown-ca --non-interactive \
    https://svn.oss.deltares.nl/repos/delft3d/tags/delft3dfm/142431/examples/12_dflowfm/test_data/e100_f02_c02-FriesianInlet_schematic_FM \
    /tmp/dflowfm-example

cd /tmp/dflowfm-example

# Run D-Flow FM simulation
dflowfm --autostartstop f34.mdu
