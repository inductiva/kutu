

FROM inductiva/kutu:base-image_v0.1.1 as build

RUN git clone https://gitlab.inria.fr/croco-ocean/croco.git && \
    #go to commit
    cd croco && \
    git checkout 7caf5b5276cc0bfbe3be07238104e88d6d40cedb && \
    git clone https://gitlab.inria.fr/croco-ocean/croco_tools.git && \
    cd croco_tools && \
    git checkout c9d570900ce69b4fd47d776eb49ebd7d3da50f1b && \
    cd /croco && \
    sed -i 's/CROCO_DIR=$PWD/CROCO_DIR=\/croco\//g' create_config.bash

COPY ./test_sim.sh /home/test_sim.sh

RUN chmod +x /home/test_sim.sh

