#!/bin/bash

make -C src_simRNN

NE=500
samp_pitch=0.1
sim_len=4.0

python3 create_1Dneuralfield_network.py $NE

python3 test_input.py $NE $sim_len $samp_pitch | ./simRNN $NE $samp_pitch

python3 plot_spike.py spikeE.csv
python3 plot_weightchange.py WEEinit.csv WEE_3.csv $NE
python3 plot_slice.py
