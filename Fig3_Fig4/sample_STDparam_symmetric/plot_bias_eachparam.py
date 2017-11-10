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
pylab.rcParams["figure.figsize"]=(6, 2)

data=numpy.loadtxt("bias_log.csv", delimiter=",")

linfit=numpy.zeros([6,4])

pylab.clf()
pylab.subplot(2,3,1)
signif=data[:,5]<0.01
nosignif=data[:,5]>0.01
pylab.plot(data[signif,0], data[signif,3], ".", markersize=2, color="black")
pylab.plot(data[nosignif,0], data[nosignif,3], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,0], data[:,3])
linfit[0,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [a*numpy.min(data[:,0])+b, a*numpy.max(data[:,0])+b], color="red")
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [0.0, 0.0], color="blue")
pylab.ylabel("Mean bias")
pylab.xlabel("Initial release probability")
#pylab.xlabel(r"$U$")

pylab.subplot(2,3,2)
signif=data[:,5]<0.01
nosignif=data[:,5]>0.01
pylab.plot(data[signif,1], data[signif,3], ".", markersize=2, color="black")
pylab.plot(data[nosignif,1], data[nosignif,3], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,1], data[:,3])
linfit[1,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [a*numpy.min(data[:,1])+b, a*numpy.max(data[:,1])+b], color="red")
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [0.0, 0.0], color="blue")
pylab.ylabel("Mean bias")
pylab.xlabel("Time constant of STD [ms]")
#pylab.xlabel(r"$\tau_\mathrm{STD}$ [ms]")

pylab.subplot(2,3,3)
signif=data[:,5]<0.01
nosignif=data[:,5]>0.01
pylab.plot(data[signif,2], data[signif,3], ".", markersize=2, color="black")
pylab.plot(data[nosignif,2], data[nosignif,3], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,2], data[:,3])
linfit[2,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,2]), numpy.max(data[:,2])], [a*numpy.min(data[:,2])+b, a*numpy.max(data[:,2])+b], color="red")
pylab.plot([numpy.min(data[:,2]), numpy.max(data[:,2])], [0.0, 0.0], color="blue")
pylab.ylabel("Mean bias")
pylab.xlabel("Time constant of STF [ms]")
#pylab.xlabel(r"$\tau_\mathrm{STF}$ [ms]")

pylab.subplot(2,3,4)
signif=data[:,7]<0.01
nosignif=data[:,7]>0.01
pylab.plot(data[signif,0], data[signif,6], ".", markersize=2, color="black")
pylab.plot(data[nosignif,0], data[nosignif,6], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,0], data[:,6])
linfit[3,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [a*numpy.min(data[:,0])+b, a*numpy.max(data[:,0])+b], color="red")
pylab.plot([numpy.min(data[:,0]), numpy.max(data[:,0])], [0.5, 0.5], color="blue")
pylab.ylim([0,1])
pylab.yticks([0,0.5,1])
pylab.ylabel("P(bias>0)")
pylab.xlabel("Initial release probability")
#pylab.xlabel(r"$U$")

pylab.subplot(2,3,5)
signif=data[:,7]<0.01
nosignif=data[:,7]>0.01
pylab.plot(data[signif,1], data[signif,6], ".", markersize=2, color="black")
pylab.plot(data[nosignif,1], data[nosignif,6], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,1], data[:,6])
linfit[4,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [a*numpy.min(data[:,1])+b, a*numpy.max(data[:,1])+b], color="red")
pylab.plot([numpy.min(data[:,1]), numpy.max(data[:,1])], [0.5, 0.5], color="blue")
pylab.ylim([0,1])
pylab.yticks([0,0.5,1])
pylab.ylabel("P(bias>0)")
pylab.xlabel("Time constant of STD [ms]")
#pylab.xlabel(r"$\tau_\mathrm{STD}$ [ms]")

pylab.subplot(2,3,6)
signif=data[:,7]<0.01
nosignif=data[:,7]>0.01
pylab.plot(data[signif,2], data[signif,6], ".", markersize=2, color="black")
pylab.plot(data[nosignif,2], data[nosignif,6], ".", markersize=2, color="grey")
a,b,r_val, p_val, stderr=scipy.stats.linregress(data[:,2], data[:,6])
linfit[5,:]=[a,b,r_val,p_val]
pylab.plot([numpy.min(data[:,2]), numpy.max(data[:,2])], [a*numpy.min(data[:,2])+b, a*numpy.max(data[:,2])+b], color="red")
pylab.plot([numpy.min(data[:,2]), numpy.max(data[:,2])], [0.5, 0.5], color="blue")
pylab.ylim([0,1])
pylab.yticks([0,0.5,1])
pylab.ylabel("P(bias>0)")
pylab.xlabel("Time constant of STF [ms]")
#pylab.xlabel(r"$\tau_\mathrm{STF}$ [ms]")

pylab.tight_layout()
pylab.savefig("bias.pdf")

numpy.savetxt("linregress_results.csv", linfit, delimiter=",")
