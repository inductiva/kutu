#!/bin/bash

mkdir /workdir
mkdir /workdir/output
mkdir /workdir/output/artifacts

cd /workdir/output/artifacts

cp -r /opt/COAWST /workdir/output/artifacts/__COAWST

cp /home/coawst-input-example/* .

create_all_sim_links

bash build_coawst.sh

mpirun --allow-run-as-root --use-hwthread-cpus -np 4 coawstM ocean_ducknc.in

rm -r  __COAWST

clean_all_sim_links
