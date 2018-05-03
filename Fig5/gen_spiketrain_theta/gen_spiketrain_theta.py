#!/usr/bin/env python3

import sys
import numpy
import scipy.special
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

def gauss(x, sigma):
    return numpy.exp(-0.5*(x/sigma)**2)/numpy.sqrt(2.0*numpy.pi)/sigma

def vonmises(x,beta):
    return numpy.exp(beta*numpy.cos(x))*0.5/numpy.pi/scipy.special.i0(beta)

neuron_num=81
simlen=1000 #ms

PFmax=0.04#kHz
PFcenter=2.0*numpy.arange(neuron_num)/float(neuron_num)-0.5
theta_phase_init=2.0*numpy.pi*numpy.random.rand()
phase_width=float(sys.argv[1])
PFwidth=0.2

rate_hist=numpy.zeros([simlen, neuron_num])
theta_hist=numpy.zeros(simlen)
spike=[]
for i in range(neuron_num):
    spike.append([])
for t in range(simlen):
    pos=float(t)/float(simlen)
    theta_phase=2.0*numpy.pi*pos*8.0+theta_phase_init
    precess=numpy.pi*(PFcenter-pos) 
    rate=PFmax*gauss(pos-PFcenter,PFwidth)*vonmises(theta_phase-precess,phase_width)
    
    theta_hist[t]=-(numpy.cos(theta_phase)+1.0)
    rate_hist[t,:]=rate
    spike_t=numpy.random.rand(neuron_num)<rate
    for i in range(neuron_num):
        if spike_t[i]:
            spike[i].append(t)

fname="spiketrain_theta_width"+str(phase_width)

rate_sigma=50.0
rate_time=numpy.arange(simlen)
meanrate=numpy.zeros([simlen, neuron_num])
for i in range(neuron_num):
    for tspike in spike[i]:
        meanrate[:,i]+=gauss(rate_time-tspike, rate_sigma)
meanpeakrate=numpy.mean(numpy.max(meanrate,axis=0))
print(meanpeakrate)

pylab.close()
pylab.figure(figsize=(3,1.5))
for i in range(neuron_num):
    pylab.plot(meanrate[:,i])
pylab.ylabel("Rate")
pylab.savefig("rate.png")

pylab.close()
pylab.figure(figsize=(2,1.5))
#pylab.subplot2grid([3,1],[0,0], rowspan=1)
#pylab.plot(theta_hist, color="black")
#pylab.axis("off")
#pylab.xticks([])
#pylab.yticks([])
#pylab.ylabel("Theta")
pylab.title("Mean peak rate="+str(int(numpy.around(meanpeakrate*1000)))+" Hz\nPhase selectivity="+str(phase_width))
#pylab.subplot2grid([3,1],[1,0], rowspan=2)
for n in range(neuron_num):
    for time in spike[n]:
        pylab.plot(time, n, ".", color="black", markersize=2)
pylab.xlim([0, 1000.0])
pylab.xticks([0, 500, 1000])
pylab.ylim([0, neuron_num+1])
pylab.yticks([1, neuron_num])
pylab.xlabel("Time [ms]")
pylab.ylabel("Neuron #")
#pylab.title(str(spike_num)+" spikes\nISI="+str(meanISI)+" ms\nspeed="+str(ms_per_neuron)+" ms", fontsize=8)
pylab.tight_layout()
pylab.savefig(fname+".svg")
