#!/usr/bin/env python3

import numpy
import pylab
import sys

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

def shift2D(mat, shift0, shift1):
    ret=numpy.roll(numpy.roll(mat, shift0, axis=0), shift1, axis=1) #torus
    #non-torus
    if shift0==1:
        ret[0,:]=0.0
    elif shift0==-1:
        ret[-1,:]=0.0
    if shift1==1:
        ret[:,0]=0.0
    elif shift1==-1:
        ret[:,-1]=0.0
    return ret

def connection_vector(weight):
    sq2=1.0/numpy.sqrt(2)
    synapse_arr=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
    synapse_num=len(synapse_arr)
    unit_vec=[[sq2,sq2],[1.0,0.0],[sq2,-sq2],[0.0,1.0],[0.0,-1.0],[-sq2,sq2],[-1.0,0.0],[-sq2,-sq2]]
    mean_vec=numpy.zeros([2,xlen,ylen])
    for i in range(synapse_num):
        shifted=shift2D(weight[i,:,:], -synapse_arr[i][0], -synapse_arr[i][1])
        mean_vec[0,:,:]=mean_vec[0,:,:]+shifted*unit_vec[i][0]
        mean_vec[1,:,:]=mean_vec[1,:,:]+shifted*unit_vec[i][1]
    return (mean_vec[0,:,:], mean_vec[1,:,:])

W=numpy.load("W_"+sys.argv[1]+".npy")
xlen=W.shape[1]
ylen=W.shape[2]

WvecX,WvecY=connection_vector(W)
WvecY=-WvecY #invert Y-axis
R=numpy.arctan2(WvecY,WvecX)
centerX=numpy.zeros([xlen, ylen])
centerY=numpy.zeros([xlen, ylen])
for i in range(xlen):
    for j in range(ylen):
        centerX[i,j]=float(i)
        centerY[i,j]=float(j)
        
pylab.clf()
pylab.quiver(centerX,centerY,WvecX,WvecY,R,scale=3)
pylab.xlim([-1, xlen])
pylab.ylim([-1, ylen])
ax=pylab.gca()
ax.invert_yaxis()
pylab.tight_layout()
pylab.savefig("vector_field.pdf")
