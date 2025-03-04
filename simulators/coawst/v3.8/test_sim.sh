#!/bin/bash

mkdir /workdir/output/artifacts

cd /workdir/output/artifacts

cp -r /opt/COAWST /workdir/output/artifacts/__COAWST

create_all_sim_links

bash build_coawst.sh

mpirun --allow-run-as-root --use-hwthread-cpus -np 4 coawstM ocean_ducknc

rm -r  __COAWST

clean_all_sim_links
