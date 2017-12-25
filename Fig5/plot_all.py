#!/usr/bin/env python3

import sys
import numpy
import pylab

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=8
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

spike1=numpy.loadtxt("taudelta5s/spikeE.csv", delimiter=",")
wbias1=numpy.loadtxt("taudelta5s/wbias.csv", delimiter=",")
spike2=numpy.loadtxt("taudelta0.5s/spikeE.csv", delimiter=",")
wbias2=numpy.loadtxt("taudelta0.5s/wbias.csv", delimiter=",")
spike3=numpy.loadtxt("taudelta0.5s_weakSTP/spikeE.csv", delimiter=",")
wbias3=numpy.loadtxt("taudelta0.5s_weakSTP/wbias.csv", delimiter=",")

maxval=numpy.max([numpy.max(spike1[:, 1:]), numpy.max(spike2[:, 1:]), numpy.max(spike3[:, 1:])])

pylab.clf()
pylab.figure(figsize=(4,5))

#activity
colormap="hot" #"jet", "bwr"

pylab.subplot2grid((5,1),(0,0), rowspan=1)
pylab.imshow(spike1[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike1[0,0]/1000.0, spike1[-1,0]/1000.0, len(spike1[0,1:]), 1])
pylab.clim([0.0, maxval])
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")
pylab.title("Condition 1: Slow weight change, strong STP", fontsize=8, color="red")

pylab.subplot2grid((5,1),(1,0), rowspan=1)
pylab.imshow(spike2[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike2[0,0]/1000.0, spike2[-1,0]/1000.0, len(spike2[0,1:]), 1])
pylab.clim([0.0, maxval])
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")
pylab.title("Condition 2: Fast weight change, strong STP", fontsize=8, color="blue")

pylab.subplot2grid((5,1),(2,0), rowspan=1)
pylab.imshow(spike3[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike3[0,0]/1000.0, spike3[-1,0]/1000.0, len(spike3[0,1:]), 1])
pylab.clim([0.0, maxval])
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")
pylab.title("Condition 3: Fast weight change, weak STP", fontsize=8, color="green")

#wbias
time=wbias1[:,0]/1000.0
wlim=70.0

pylab.subplot2grid((5,1),(3,0), rowspan=1)
pylab.plot(time, wbias1[:,1], label="Condition 1", color="red")
pylab.plot(time, wbias2[:,1], label="Condition 2", color="blue")
pylab.plot(time, wbias3[:,1], label="Condition 3", color="green")
pylab.plot(time, time*0.0, "--", color="black")
pylab.ylabel("Weight bias\n(Neuron #100)")
pylab.ylim([-wlim, wlim])
pylab.yticks([0.0])
pylab.xticks([])
#pylab.xlabel("Time [s]")

pylab.subplot2grid((5,1),(4,0), rowspan=1)
pylab.plot(time, wbias1[:,2], label="Condition 1", color="red")
pylab.plot(time, wbias2[:,2], label="Condition 2", color="blue")
pylab.plot(time, wbias3[:,2], label="Condition 3", color="green")
pylab.plot(time, time*0.0, "--", color="black")
pylab.ylabel("Weight bias\n(Neuron #400)")
pylab.ylim([-wlim, wlim])
pylab.yticks([0.0])
#pylab.xticks([])
pylab.xlabel("Time [s]")

pylab.tight_layout()
pylab.savefig("wbias_change.pdf")
