#!/usr/bin/env python3

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

data=numpy.loadtxt(sys.argv[1], delimiter=",")
pos=numpy.loadtxt(sys.argv[2], delimiter=",")

time=data[:,0]
data=data[:,1:]*1000.0 #kHz>Hz
pos=pos[:,1:]
maxdata=200.0
data[data>maxdata]=maxdata

pylab.clf()
pylab.imshow(data.T, interpolation="none", aspect="auto", extent=[time[0], time[-1], data.shape[1], 0], cmap="hot")
pylab.clim([0.0, maxdata])
pylab.plot(time,20*numpy.ones_like(time),"--",color="white")
pylab.plot(time,60*numpy.ones_like(time),"--",color="white")
pylab.xlabel("Time [s]")
pylab.ylabel("Neuron #")
ax=pylab.gca()
ax.invert_yaxis()
pylab.colorbar()
pylab.tight_layout()

pylab.savefig("plot.pdf")

part_len=15*100
part_num=int(len(time)//part_len)
for i in range(part_num):
    index=numpy.arange(part_len*i, part_len*(i+1))
    pylab.clf()
    #pylab.subplot(2,1,1)
    pylab.subplot2grid((3,1),(0,0),rowspan=1)
    pylab.plot(time[index],pos[index], ".",markersize=2)
    pylab.plot(time[index],1*numpy.ones_like(time[index]),"--",color="black")
    pylab.plot(time[index],3*numpy.ones_like(time[index]),"--",color="black")
    pylab.ylim([-0.1, 5.1])
    pylab.yticks([0, 1, 3, 5])
    pylab.xlim([time[index[0]], time[index[-1]]])
    pylab.xticks([])
    pylab.ylabel("Position")

    #pylab.subplot(2,1,2)
    pylab.subplot2grid((3,1),(1,0),rowspan=2)
    pylab.imshow(data[index,:].T, interpolation="none", aspect="auto", extent=[time[index[0]], time[index[-1]], data.shape[1], 0], cmap="hot")
    pylab.clim([0.0, maxdata])
    pylab.plot(time[index],20*numpy.ones_like(time[index]),"--",color="white")
    pylab.plot(time[index],60*numpy.ones_like(time[index]),"--",color="white")
    pylab.xlabel("Time [s]")
    pylab.ylabel("Neuron #")
    pylab.xlim([time[index[0]], time[index[-1]]])
    pylab.xticks([time[index[0]], time[index[-1]]])
    ax=pylab.gca()
    ax.invert_yaxis()
    #pylab.colorbar()
    pylab.tight_layout()
    
    pylab.savefig("plot_part"+str(i)+".pdf")
