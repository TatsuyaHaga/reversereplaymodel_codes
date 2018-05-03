#!/usr/bin/env python3

import matplotlib
matplotlib.use("Agg")
import numpy
import pylab
import sys
import os

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
pylab.rcParams["figure.figsize"]=(2, 2)

pos=numpy.loadtxt(sys.argv[1], delimiter=",")
xlen=int(sys.argv[2])
ylen=int(sys.argv[3])

time=pos[:,0]
pos=pos[:,1:]

pylab.close()
pylab.plot(pos[0,1], pos[0,0], "o", color="blue")
pylab.plot(pos[-1,1], pos[-1,0], "o", color="red")
pylab.plot(pos[:,1], pos[:,0], color="black")
pylab.gca().invert_yaxis()
pylab.xlim([0,xlen-1])
pylab.ylim([ylen-1,0])
pylab.xticks([])
pylab.yticks([])
pylab.tight_layout()
pylab.savefig("trajectory.svg")
