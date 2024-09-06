#!/bin/bash

cd /home/fvcom-input-example/run

fvcom --CASENAME=tst

cd /home/fvcom-input-example-wet-dry/run

fvcom_ESTUARY --CASENAME=tst