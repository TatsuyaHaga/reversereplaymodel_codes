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
pylab.rcParams["figure.figsize"]=(3, 3)

#activity
colormap="hot" #"jet", "bwr"

spike=numpy.loadtxt("spikeE.csv", delimiter=",")

pylab.clf()
pylab.figure(figsize=(6,4))
pylab.subplot2grid((4,1),(0,0), rowspan=2)
pylab.imshow(spike[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike[0,0]/1000.0, spike[-1,0]/1000.0, len(spike[0,1:]), 1])
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
#pylab.colorbar()
pylab.xticks([])
#pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")

#wbias
wbias=numpy.loadtxt("wbias.csv", delimiter=",")
time=wbias[:,0]/1000.0
wlim=70.0

pylab.subplot2grid((4,1),(2,0), rowspan=1)
pylab.plot(time, wbias[:,1], label="Neuron 100", color="blue")
pylab.plot(time, time*0.0, "--", color="black")
pylab.ylabel("Weight bias\n(Neuron 100)")
pylab.ylim([-wlim, wlim])
pylab.yticks([0.0])
pylab.xticks([])
#pylab.xlabel("Time [s]")

pylab.subplot2grid((4,1),(3,0), rowspan=1)
pylab.plot(time, wbias[:,2], label="Neuron 400", color="red")
pylab.plot(time, time*0.0, "--", color="black")
pylab.ylabel("Weight bias\n(Neuron 400)")
pylab.ylim([-wlim, wlim])
pylab.yticks([0.0])
#pylab.xticks([])
pylab.xlabel("Time [s]")

pylab.tight_layout()
pylab.savefig("wbias_change.pdf")
