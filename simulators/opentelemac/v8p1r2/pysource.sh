# TELEMAC Environment Script

### TELEMAC settings
export HOMETEL=/opt/telemac-mascaret
export PATH=$HOMETEL/scripts/python3:$PATH
export SYSTELCFG=$HOMETEL/configs/systel.cfg
export USETELCFG=gfortranHPC
export SOURCEFILE=$HOMETEL/configs/pysource.sh

### Python
export PYTHONUNBUFFERED='true'

### API
export PYTHONPATH=$HOMETEL/scripts/python3:$PYTHONPATH
export LD_LIBRARY_PATH=$HOMETEL/builds/$USETELCFG/lib:$HOMETEL/builds/$USETELCFG/wrap_api/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$HOMETEL/builds/$USETELCFG/wrap_api/lib:$PYTHONPATH

### METIS (Ubuntu package path)
export METISHOME=/usr
