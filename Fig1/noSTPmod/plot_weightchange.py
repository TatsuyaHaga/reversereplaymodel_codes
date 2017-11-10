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
pylab.rcParams["figure.figsize"]=(3, 2)

wbefore=numpy.loadtxt(sys.argv[1], delimiter=",")
wafter=numpy.loadtxt(sys.argv[2], delimiter=",")
neuron_num=int(sys.argv[3])
pre_neuron=int(neuron_num/2)

wbefore_post=numpy.zeros(neuron_num)
wafter_post=numpy.zeros(neuron_num)
for i in range(len(wbefore)):
    if wbefore[i,0]==pre_neuron:
        x=int(wbefore[i,1])
        wbefore_post[x]=wbefore[i,2]
    if wafter[i,0]==pre_neuron:
        x=int(wafter[i,1])
        wafter_post[x]=wafter[i,2]

colormap="jet" #"bwr"
pylab.clf()
wchange=wafter_post-wbefore_post
xarr=numpy.arange(pre_neuron-50,pre_neuron+50)

pylab.subplot2grid((3,1), (0,0), rowspan=2)
pylab.plot(xarr, wbefore_post[xarr], label="before", color="black")
pylab.plot(xarr, wafter_post[xarr], label="after", color="red")
pylab.plot(pre_neuron, 0, "o", color="black")
pylab.ylabel("Synaptic weights")
pylab.ylim([0.0, 25.0])
pylab.yticks([0.0, 25.0])
pylab.xticks([])
pylab.legend()

pylab.subplot2grid((3,1), (2,0), rowspan=1)
pylab.plot(xarr, wchange[xarr], label="change", color="blue")
pylab.plot(pre_neuron, 0, "o", color="black")
pylab.ylim([0.0, 3.0])
pylab.yticks([0.0, 3.0])
pylab.xlabel("Neuron #")
pylab.ylabel("Change")

pylab.tight_layout()
pylab.savefig("weight_change.svg")
