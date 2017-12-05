#!/usr/bin/python

import numpy
import pylab

pylab.rcParams["font.size"]=7
pylab.rcParams["legend.fontsize"]=7
#pylab.rcParams["lines.linewidth"]=1
#pylab.rcParams["axes.linewidth"]=2
#pylab.rcParams["axes.labelsize"]="large"
#pylab.rcParams["axes.labelweight"]="bold"
pylab.rcParams["xtick.major.size"]=0
pylab.rcParams["xtick.minor.size"]=0
pylab.rcParams["ytick.major.size"]=0
pylab.rcParams["ytick.minor.size"]=0
#pylab.rcParams["xtick.direction"]="out"
#pylab.rcParams["ytick.direction"]="out"
pylab.rcParams["figure.figsize"]=(3, 2)

#activity
colormap="jet" #"bwr"
xE=numpy.loadtxt("spikeE.csv", delimiter=",")
xE_STD=numpy.loadtxt("xSTD.csv", delimiter=",")
ADP=numpy.loadtxt("ADP.csv", delimiter=",")

time=30
start=100
end=400
xtick=range(start+1,end+1)

pylab.clf()
pylab.subplot(2,1,1)
pylab.plot(xtick, xE[time, xtick], label="Activity")
pylab.plot(xtick, ADP[time, xtick], label="ADP")
pylab.legend()
pylab.ylabel("Activity")
pylab.xticks([])
pylab.ylim([0.0, 0.15])
pylab.yticks([0.0, 0.15])

pylab.subplot(2,1,2)
pylab.plot(xtick, xE_STD[time, xtick], label="STD")
pylab.plot(xtick, [1.0]*len(xtick), "--", color="black")
pylab.ylabel("Amount of\nneurotransmitter")
pylab.xlabel("Neuron #")
pylab.ylim([0.0, 1.1])
pylab.yticks([0.0, 1.0])

pylab.tight_layout()
pylab.savefig("x_slice.svg")
