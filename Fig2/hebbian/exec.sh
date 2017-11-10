#!/bin/bash

make -C src_simRNN

NE=500
samp_pitch=0.01
sim_len=4.0
STDPTYPE=1 #1:Hebbian 2:anti-Hebbian 3:symmetric else:no plasticity
STDPMOD=1 #STDP modulation 1:ON 0:OFF

python3 create_1Dneuralfield_network.py $NE

date
python3 test_input.py $NE $sim_len $samp_pitch | ./simRNN $NE $samp_pitch $STDPTYPE $STDPMOD
date

python3 plot_spike.py spikeE.csv
python3 plot_weightchange.py WEEinit.csv WEE_3.csv $NE
