#!/usr/bin/env python3

import sys
import numpy
import csv

#neurons
exc_neuron_num=int(sys.argv[1])

#soma exc synapse
EEmax=0.3 #RS:0.3 IB:0.2
EEwidth=5.0 #5.0 is min
AMPA_NMDA_ratio=0.2

#E<-E
f=open("WEEinit.csv","w")
writer=csv.writer(f, delimiter=",",lineterminator="\n")
for toN in range(exc_neuron_num):
    for fromN in range(exc_neuron_num):
        dif=numpy.abs(toN-fromN)
        #dif=numpy.min([numpy.abs(toN-fromN), exc_neuron_num-numpy.abs(toN-fromN)])
        if dif!=0:
            w=EEmax*numpy.exp(-dif/EEwidth)
            writer.writerow([fromN, toN, w, w*AMPA_NMDA_ratio])
f.close()
