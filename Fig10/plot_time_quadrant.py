#!/usr/bin/env python3

import sys
import os
import numpy
import scipy.stats
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

def calc_quad(dirname, Ntrial):
    quad_ratio=[]
    for i in range(int(Ntrial)):
        set_info=numpy.loadtxt(dirname+"/trial"+str(i+1)+"/time_explore.csv", delimiter=",")
        for sets in [6,11,16]:
            pos=numpy.loadtxt(dirname+"/trial"+str(i+1)+"/pos_set"+str(sets)+".csv", delimiter=",")
            prev_reward=set_info[sets-2, [-2,-1]]
            time=pos[:,0]-pos[0,0]
            pos=pos[:,1:]
            startlen=3.0 #s
            endtime=startlen+set_info[sets-1,1]
            filtrun=(time>=startlen)*(time<=endtime)
            pos=pos[filtrun,:]
            in_quad_prevreward=(pos[:,0]>=prev_reward[0]-10)*(pos[:,0]<=prev_reward[0]+10)*(pos[:,1]>=prev_reward[1]-10)*(pos[:,1]<=prev_reward[1]+10)
            if len(in_quad_prevreward)>0:
                quad_ratio.append(numpy.sum(in_quad_prevreward)/len(in_quad_prevreward))
    return numpy.array(quad_ratio)*100.0

quad_ON=calc_quad("learningON", int(sys.argv[1]))
quad_OFF=calc_quad("learningOFF", int(sys.argv[2]))

pylab.close()
pylab.figure(figsize=(1.5,2.5))
pylab.plot([0]*len(quad_ON), quad_ON, ".", color="gray")
pylab.plot([0], numpy.mean(quad_ON), "o", color="black")
pylab.plot([1]*len(quad_OFF), quad_OFF, ".", color="gray")
pylab.plot([1], numpy.mean(quad_OFF), "o", color="black")
pylab.xlim([-0.5,1.5])
pylab.xticks([0,1], ["learning ON", "learning OFF"], rotation="vertical")
pylab.ylim([0,100])
pylab.yticks([0,50,100])
pylab.ylabel("Percent time\naround previous reward")
pylab.tight_layout()
pylab.savefig("time_quad_compare.svg")

stattest_func=scipy.stats.ranksums
stat=numpy.zeros([1,2])
stat[0,:]=stattest_func(quad_ON, quad_OFF)
numpy.savetxt("time_quadrant_stat_ranksum.csv", stat, delimiter=",")

stattest_func=scipy.stats.shapiro
stat=numpy.zeros([2,2])
stat[0,:]=stattest_func(quad_ON)
stat[1,:]=stattest_func(quad_OFF)
numpy.savetxt("time_quadrant_stat_shapiro.csv", stat, delimiter=",")

