#!/bin/bash

for N in `seq ${1} ${2}`
do
    avconv -y -r 50 -i img_set${N}/img%04d.png -vsync cfr movie_set${N}.avi
done
