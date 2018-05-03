#!/usr/bin/env python3

import sys
import os
import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

data=[numpy.loadtxt("trial"+str(i+1)+"/time_explore.csv", delimiter=",")[:,1] for i in range(int(sys.argv[1]))]
data=numpy.vstack(data).T
x=numpy.arange(data.shape[0])+1
mean=numpy.mean(data, axis=1)
std=numpy.std(data, axis=1)

pylab.close()
pylab.figure(figsize=(2.5,2))
for i in range(data.shape[1]):
    pylab.plot(x, data[:,i], ".-", color="gray")
pylab.plot(x, mean, "o-", color="black")
#pylab.errorbar(x, mean, yerr=std, color="black")
pylab.xlim([0.5,20.5])
pylab.ylim([0,300])
pylab.yticks([0,150,300])
pylab.ylabel("Latency [s]")
pylab.xlabel("Trials")
pylab.tight_layout()
pylab.savefig("time_explore.svg")
