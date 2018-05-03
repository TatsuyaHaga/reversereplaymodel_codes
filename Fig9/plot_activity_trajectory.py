#!/usr/bin/env python3

import numpy
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

rate=numpy.loadtxt("rate.csv", delimiter=",")
time=rate[:,0]
time_max=int(numpy.ceil(numpy.max(time)))
rate=rate[:,1:]
xlen=50
ylen=50

centerX=numpy.zeros([xlen, ylen])
centerY=numpy.zeros([xlen, ylen])
for i in range(xlen):
    for j in range(ylen):
        centerX[i,j]=float(i)
        centerY[i,j]=float(j)
        
centerX=centerX.reshape(xlen*ylen)
centerY=centerY.reshape(xlen*ylen)

pylab.close()
pylab.figure(figsize=(3,3))
for i in range(time_max):
  rate_cut=rate[(i<=time)*(time<i+1),:]
  cmassX=[]
  cmassY=[]
  for r in rate_cut:
    if numpy.max(r)>=0.01:
      rsum=numpy.sum(r)
      cmassX.append(centerX@r/rsum)
      cmassY.append(centerY@r/rsum)
  pylab.plot(cmassX,cmassY,color="black")
pylab.plot(xlen/2,ylen/2,"o",color="blue")
pylab.xlim([-1, xlen])
pylab.ylim([-1, ylen])
ax=pylab.gca()
ax.invert_yaxis()
pylab.tight_layout()
pylab.savefig("activity_trajectory.pdf")
