#!/bin/bash

N_ON=10
N_OFF=10

cd learningON/
python3 ../plot_time_explore.py $N_ON
mv time_explore.svg ../time_explore_learningON.svg
cd ../

cd learningOFF/
python3 ../plot_time_explore.py $N_OFF
mv time_explore.svg ../time_explore_learningOFF.svg
cd ../

python3 plot_time_explore_compare.py $N_ON $N_OFF
python3 plot_angle.py $N_ON $N_OFF
python3 plot_angle_diffeach.py $N_ON $N_OFF
python3 plot_time_quadrant.py $N_ON $N_OFF
