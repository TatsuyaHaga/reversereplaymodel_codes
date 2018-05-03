#!/bin/bash

python3 sim.py
python3 plot_1Dtime.py rate1D.csv pos1D.csv

python3 plot_vector_field.py init
mv vector_field.pdf vector_field_init.pdf
python3 plot_vector_field.py end
mv vector_field.pdf vector_field_end.pdf

#python3 plot_2Dmovie_pos.py rate.csv pos.csv 50 50
