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
#pylab.rcParams["figure.figsize"]=(3, 3)

#activity
colormap="hot" #"jet", "bwr"

spike=numpy.loadtxt(sys.argv[1], delimiter=",")

pylab.clf()
pylab.figure(figsize=(3,2))
pylab.imshow(spike[:, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike[0,0]/1000.0, spike[-1,0]/1000.0, len(spike[0,1:]), 1])
#limit=numpy.max(numpy.abs(xE[:,1:]))
#pylab.clim([-limit, limit])
pylab.colorbar()
pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")
pylab.tight_layout()
pylab.savefig("spike.pdf")

#part
part_len=10*100
part_num=int(len(spike[:,0])//part_len)
for i in range(part_num):
    pylab.clf()
    pylab.figure(figsize=(3,4))
    pylab.subplot(2,1,1)
    pylab.imshow(spike[i*part_len:(i+1)*part_len, 1:].T, aspect="auto", interpolation="none", cmap=colormap, extent=[spike[i*part_len,0]/1000.0, spike[(i+1)*part_len-1,0]/1000.0, len(spike[0,1:]), 1])
    pylab.colorbar()
    pylab.xlabel("Time [s]")
    pylab.ylabel("Neuron #")
    pylab.tight_layout()
    
    pylab.subplot(2,1,2)
    pylab.plot(spike[i*part_len:(i+1)*part_len, 0], numpy.mean(spike[i*part_len:(i+1)*part_len, 1:]*1000.0, axis=1))
    pylab.xlabel("Time [s]")
    pylab.ylabel("Mean rate [Hz]")
    pylab.tight_layout()
    
    pylab.savefig("spike_part"+str(i)+".pdf")
