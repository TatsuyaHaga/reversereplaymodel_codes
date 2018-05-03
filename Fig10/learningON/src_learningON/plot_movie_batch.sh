#!/bin/bash

for N in `seq 1 5`
do
    python3 plot_2Dmovie_pos.py rate_set${N}.csv pos_set${N}.csv 50 50
    mv movie.avi movie_set${N}.avi
done
