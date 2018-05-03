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
#pylab.rcParams["figure.figsize"]=(3, 3)

data=numpy.loadtxt(sys.argv[1], delimiter=",")
pos=numpy.loadtxt(sys.argv[2], delimiter=",")
xlen=int(sys.argv[3])
ylen=int(sys.argv[4])

time=data[:,0]
data=data[:,1:]*1000.0
pos=pos[:,1:]

data_max=200.0
data[data>data_max]=data_max
data_min=numpy.min(data)

plot_pitch=1

count=0
for t in range(len(time)):
    if (t*10)/len(time)==(t*10)//len(time):
        print((t*100)//len(time),"%...")
    if t%plot_pitch==0:
        pylab.clf()
        pylab.imshow((data[t,:].reshape(xlen,ylen)).T, vmin=data_min, vmax=data_max, interpolation="none", cmap="jet")
        pylab.plot(pos[t,0], pos[t,1], "o", color="white")
        pylab.xlim([0,xlen-1])
        pylab.ylim([ylen-1,0])
        pylab.colorbar()
        pylab.title(str(numpy.round(time[t],decimals=1))+" s")
        pylab.tight_layout()

        if count<10:
            tag="000"+str(count)
        elif count<100:
            tag="00"+str(count)
        elif count<1000:
            tag="0"+str(count)
        elif count<10000:
            tag=str(count)
        pylab.savefig("img"+tag+".png")
        count=count+1

#create movie
#os.system("avconv -y -r 25 -i img%04d.png -vsync cfr movie.avi")
os.system("avconv -y -r 50 -i img%04d.png -vsync cfr movie.avi")
os.system("rm img*.png")
