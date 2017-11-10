#!/usr/bin/env python3

import numpy
import pylab
import scipy.stats

pylab.rcParams["font.size"]=8
pylab.rcParams["legend.fontsize"]=8
#pylab.rcParams["lines.linewidth"]=1
#pylab.rcParams["axes.linewidth"]=2
#pylab.rcParams["axes.labelsize"]="small"
#pylab.rcParams["axes.labelweight"]="bold"
pylab.rcParams["xtick.major.size"]=0
pylab.rcParams["xtick.minor.size"]=0
pylab.rcParams["ytick.major.size"]=0
pylab.rcParams["ytick.minor.size"]=0
#pylab.rcParams["xtick.direction"]="out"
#pylab.rcParams["ytick.direction"]="out"
pylab.rcParams["figure.figsize"]=(3, 2)

data=numpy.loadtxt("bias_log.csv", delimiter=",")

linfit=numpy.zeros([4,4])

pylab.clf()
pylab.subplot(2,2,1)
signif=data[:,4]<0.01
nosignif=data[:,4]>=0.01
pylab.plot(data[signif,0], data[signif,2], ".", markersize=2, color="black")
pylab.plot(data[nosignif,0], data[nosignif,2], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,0], data[:,2])
linfit[0,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [a*numpy.min(data[:,0])+b, a*numpy.max(data[:,0])+b], color="red")
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [0.0, 0.0], color="blue")
pylab.xticks([])
pylab.ylabel("Mean bias")
#pylab.xlabel("ISI [ms]")

pylab.subplot(2,2,2)
signif=data[:,4]<0.01
nosignif=data[:,4]>=0.01
pylab.plot(data[signif,1], data[signif,2], ".", markersize=2, color="black")
pylab.plot(data[nosignif,1], data[nosignif,2], ".", markersize=2, color="grey")
a,b,r_val,p_val,stderr=scipy.stats.linregress(data[:,1], data[:,2])
linfit[1,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [a*numpy.min(data[:,1])+b, a*numpy.max(data[:,1])+b], color="red")
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [0.0, 0.0], color="blue")
pylab.xticks([])
pylab.yticks([])
#pylab.ylabel("Mean bias")
#pylab.xlabel("Speed [ms/cell]")

pylab.subplot(2,2,3)
signif=data[:,6]<0.01
nosignif=data[:,6]>=0.01
pylab.plot(data[signif,0], data[signif,5], ".", markersize=2, color="black")
pylab.plot(data[nosignif,0], data[nosignif,5], ".", markersize=2, color="grey")
a,b,r_val,p_val,stderr=scipy.stats.linregress(data[:,0], data[:,5])
linfit[2,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [a*numpy.min(data[:,0])+b, a*numpy.max(data[:,0])+b], color="red")
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [0.5, 0.5], color="blue")
pylab.xticks([5,10,20,30,40,50])
pylab.ylim([0,1])
pylab.yticks([0,0.5,1])
pylab.ylabel("P(bias>0)")
pylab.xlabel("ISI [ms]")

pylab.subplot(2,2,4)
signif=data[:,6]<0.01
nosignif=data[:,6]>=0.01
pylab.plot(data[signif,1], data[signif,5], ".", markersize=2, color="black")
pylab.plot(data[nosignif,1], data[nosignif,5], ".", markersize=2, color="grey")
a,b,r_val,p_val,stderr=scipy.stats.linregress(data[:,1], data[:,5])
linfit[3,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [a*numpy.min(data[:,1])+b, a*numpy.max(data[:,1])+b], color="red")
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [0.5, 0.5], color="blue")
pylab.xticks([5,10,20,30,40,50])
pylab.ylim([0,1])
#pylab.yticks([0,0.5,1])
pylab.yticks([])
#pylab.ylabel("P(bias>0)")
pylab.xlabel("Speed [ms/cell]")

pylab.tight_layout()
pylab.savefig("bias.pdf")

numpy.savetxt("linregress_results.csv", linfit, delimiter=",")
