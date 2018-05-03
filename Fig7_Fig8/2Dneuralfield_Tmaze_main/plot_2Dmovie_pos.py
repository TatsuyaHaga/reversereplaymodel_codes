#!/usr/bin/env python3

import matplotlib
matplotlib.use("Agg")
import numpy
import pylab
import sys
import os

#pylab.rcParams["font.size"]=8
#pylab.rcParams["legend.fontsize"]=8
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
colormap="gist_heat_r"

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

plot_pitch=2

posA=[0.5*float(xlen), 0.3*float(ylen)]
posB=[0.5*float(xlen), 0.7*float(ylen)]
posC1=[0.9*float(xlen), 0.7*float(ylen)]
posD1=[0.9*float(xlen), 0.3*float(ylen)]
posC2=[0.1*float(xlen), 0.7*float(ylen)]
posD2=[0.1*float(xlen), 0.3*float(ylen)]

count=0
for t in range(len(time)):
    if (t*10)/len(time)==(t*10)//len(time):
        print((t*100)//len(time),"%...")
    if t%plot_pitch==0:
        trialnum=int(1+time[t]/15)
        if trialnum%2==1:
            goal="D1"
        else:
            goal="D2"
        explain=""

        pylab.close()
        pylab.imshow((data[t,:].reshape(xlen,ylen)).T, vmin=data_min, vmax=data_max, interpolation="none", cmap=colormap)
        pylab.plot([posA[0],posB[0]], [posA[1], posB[1]], color="gray")
        pylab.plot([posB[0],posC1[0]], [posB[1], posC1[1]], color="gray")
        pylab.plot([posB[0],posC2[0]], [posB[1], posC2[1]], color="gray")
        pylab.plot([posC1[0],posD1[0]], [posC1[1], posD1[1]], color="gray")
        pylab.plot([posC2[0],posD2[0]], [posC2[1], posD2[1]], color="gray")
        pylab.text(posA[0],posA[1],"A")
        pylab.text(posB[0],posB[1],"B")
        pylab.text(posC1[0],posC1[1],"C1")
        pylab.text(posC2[0],posC2[1],"C2")
        pylab.text(posD1[0],posD1[1],"D1")
        pylab.text(posD2[0],posD2[1],"D2 (reward)")
        pylab.plot(pos[t,0], pos[t,1], "o", color="blue")
        pylab.xlim([0,xlen-1])
        pylab.ylim([ylen-1,0])
        pylab.colorbar()
        pylab.title(str(numpy.round(time[t],decimals=1))+" s Trial "+str(trialnum)+": travel A -> "+goal)
        pylab.text(25,48,explain, verticalalignment="bottom", horizontalalignment="center", fontsize=11)
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
#os.system("avconv -r 25 -i img%04d.png -vsync cfr movie.avi")
os.system("avconv -r 50 -i img%04d.png -vsync cfr movie.avi")
os.system("rm img*.png")
