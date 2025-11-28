#!/bin/bash

# Install curl, unzip and ca-certificates
apt-get update && apt-get install -y --no-install-recommends curl unzip ca-certificates

# Download and unzip D-Flow FM example
curl -L -o /tmp/delft3dfm-input-example.zip https://storage.googleapis.com/inductiva-api-demo-files/delft3dfm-input-example.zip
unzip /tmp/delft3dfm-input-example.zip -d /tmp

cd /tmp/delft3dfm-input-example

# Run D-Flow FM simulation
dflowfm --autostartstop f34.mdu
