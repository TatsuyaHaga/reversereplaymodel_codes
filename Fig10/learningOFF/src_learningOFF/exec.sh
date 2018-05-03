#!/bin/bash

python3 sim.py

python3 plot_vector_field.py init
mv vector_field.pdf vector_field_init.pdf
python3 plot_vector_field.py end
mv vector_field.pdf vector_field_end.pdf

for N in `seq 1 20`
do
    python3 plot_trajectory.py pos_set${N}.csv 50 50
    mv trajectory.svg trajectory_set${N}.svg
done

python3 calc_angle.py
#python3 plot_img_formovie_mp.py 1 20
