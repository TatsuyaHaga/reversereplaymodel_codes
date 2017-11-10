#!/bin/bash

SAMPLE_PER_PROCESS=250
N_PROCESS=4

for STDPmode in symmetric
do
    for STDPcombi in alltoall
    do
	for Nspike in 2 3 4 5
	do
	    DIR=${STDPmode}_${STDPcombi}_${Nspike}spike
	    mkdir ${DIR}
	    cp reverse_eval_random.py ${DIR}
	    cd ${DIR}
	    python3 reverse_eval_random.py ${Nspike} ${STDPmode} ${STDPcombi} ${SAMPLE_PER_PROCESS} ${N_PROCESS}
	    python3 ../plot_bias_eachparam.py
	    cd ../
	done
    done
done


