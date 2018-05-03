#!/usr/bin/env python3

import matplotlib
matplotlib.use("Agg")
import numpy
import pylab
import sys
import os
import multiprocessing

def plot(dirname, data, pos, xlen, ylen):
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

    time=data[:,0]
    data=data[:,1:]*1000.0
    pos=pos[:,1:]

    data_max=200.0
    data[data>data_max]=data_max
    data_min=numpy.min(data)

    plot_pitch=1

    count=0
    for t in range(len(time)):
        #if (t*10)/len(time)==(t*10)//len(time):
        #    print((t*100)//len(time),"%...")
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
            if len(dirname)>0:
                pylab.savefig(dirname+"/img"+tag+".png")
            else:
                pylab.savefig("img"+tag+".png")
            count=count+1


if __name__=="__main__":
    xlen=50
    ylen=50

    data_begin=int(sys.argv[1])
    data_end=int(sys.argv[2])

    process_arr=[]
    data_arr=[]
    pos_arr=[]
    Nprocess=0
    for i in range(data_begin, data_end+1):
        dirname="img_set"+str(i)
        os.system("mkdir "+dirname)
        data_arr.append(numpy.loadtxt("rate_set"+str(i)+".csv", delimiter=","))
        pos_arr.append(numpy.loadtxt("pos_set"+str(i)+".csv", delimiter=","))
        process_arr.append(multiprocessing.Process(target=plot, args=(dirname, data_arr[Nprocess], pos_arr[Nprocess], xlen, ylen)))
        process_arr[Nprocess].start()
        Nprocess+=1

    for i in range(Nprocess):
        process_arr[i].join()

    print("done.")
