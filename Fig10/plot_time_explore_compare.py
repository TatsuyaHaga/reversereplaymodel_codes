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

#nonrandom
data=[numpy.loadtxt("learningON/trial"+str(i+1)+"/time_explore.csv", delimiter=",")[:,1] for i in range(int(sys.argv[1]))]
data=numpy.vstack(data).T
data_novel=data[[5,10,15],:].flatten()
data_repeat=data[[1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19],:].flatten()
#data_first=data[0,:]

#random
data=[numpy.loadtxt("learningOFF/trial"+str(i+1)+"/time_explore.csv", delimiter=",")[:,1] for i in range(int(sys.argv[2]))]
data=numpy.vstack(data).T
data_random=data.flatten()

pylab.close()
pylab.figure(figsize=(2,2))
pylab.plot([1]*len(data_novel), data_novel, ".", color="gray")
pylab.plot([1], numpy.mean(data_novel), "o", color="black")
pylab.plot([2]*len(data_repeat), data_repeat, ".", color="gray")
pylab.plot([2], numpy.mean(data_repeat), "o", color="black")
pylab.plot([3]*len(data_random), data_random, ".", color="gray")
pylab.plot([3], numpy.mean(data_random), "o", color="black")
pylab.xlim([0.5,3.5])
pylab.ylim([0,300])
pylab.yticks([0,150,300])
pylab.ylabel("Latency [s]")
pylab.xticks([1,2,3],["SWITCH", "REPEAT", "CONTROL"], rotation="vertical")
pylab.tight_layout()
pylab.savefig("time_explore_compare.svg")

#statistical test
stattest_func=scipy.stats.ranksums
stat=numpy.zeros([3,2])
stat[0,:]=stattest_func(data_novel, data_repeat)
stat[1,:]=stattest_func(data_repeat, data_random)
stat[2,:]=stattest_func(data_novel, data_random)
numpy.savetxt("time_explore_stat_ranksum.csv", stat, delimiter=",")

stattest_func=scipy.stats.shapiro
stat=numpy.zeros([3,2])
stat[0,:]=stattest_func(data_novel)
stat[1,:]=stattest_func(data_repeat)
stat[2,:]=stattest_func(data_novel)
numpy.savetxt("time_explore_stat_shapiro.csv", stat, delimiter=",")

