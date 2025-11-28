#!/bin/bash

# Install curl, unzip and ca-certificates
apt-get update && apt-get install -y --no-install-recommends curl unzip ca-certificates

# Download and unzip D-Flow FM example
curl -L -o /tmp/dflowfm-example.zip https://storage.googleapis.com/inductiva-api-demo-files/delft3dfm-input-example.zip
unzip /tmp/dflowfm-example.zip -d /tmp

cd /tmp/dflowfm-example

# Run D-Flow FM simulation
dflowfm --autostartstop f34.mdu
