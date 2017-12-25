#!/usr/bin/env python3

import sys
import csv
import numpy

out=csv.writer(sys.stdout, delimiter=",")

N=int(sys.argv[1])
sim_len_sec=float(sys.argv[2])
samp_pitch=float(sys.argv[3])
sim_len=int(sim_len_sec*1000.0/samp_pitch)
input_amp=5.0
time_stim=1000.0

data=numpy.zeros(N)
for t in range(1, sim_len+1):
    time_ms=float(t)*samp_pitch
    time_set=time_ms%time_stim
    data[:]=0.0
    if time_set<10.0:
        if time_ms<5.0*1000.0:
            data[0:10]=input_amp
        elif time_ms>10.0*1000.0:
            data[int(N//2)-5:int(N//2)+5]=input_amp
            #data[-10:]=input_amp
        
    out.writerow(data)
