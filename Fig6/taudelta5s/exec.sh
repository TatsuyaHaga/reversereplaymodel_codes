#!/bin/bash

make -C src_simRNN

NE=500
samp_pitch=1.0 #0.1
sim_len=30.0

python3 create_1Dneuralfield_network.py $NE

date
python3 test_input.py $NE $sim_len $samp_pitch | ./simRNN $NE $samp_pitch
date

python3 plot.py
