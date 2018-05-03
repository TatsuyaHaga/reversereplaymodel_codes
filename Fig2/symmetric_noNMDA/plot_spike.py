#!/usr/bin/env python3

import sys
import numpy
import matplotlib
matplotlib.use("Agg")
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
#pylab.rcParams["figure.figsize"]=(3, 3)

#activity
colormap="gist_heat_r"

spike=numpy.loadtxt(sys.argv[1], delimiter=",")
time=spike[:,0]/1000.0
spike=spike[:,1:]

pylab.clf()
pylab.figure(figsize=(3,2))
pylab.imshow(spike.T, aspect="auto", interpolation="none", cmap=colormap, extent=[time[0], time[-1], len(spike[0]), 1])
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
pylab.colorbar()
pylab.xticks([0,1,2,3,4])
pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")
pylab.tight_layout()
pylab.savefig("spike.pdf")

