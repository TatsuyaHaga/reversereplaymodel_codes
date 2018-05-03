#!/usr/bin/env python3

import sys
import numpy
import scipy.stats
import matplotlib
matplotlib.use("Agg")
import pylab
import seaborn
seaborn.set(context="paper", style="white", palette="deep")

Ntrial_nonrandom=int(sys.argv[1])
Ntrial_random=int(sys.argv[2])

angle_novel=[numpy.load("learningON/trial"+str(i)+"/angle_novel.npy") for i in range(1, Ntrial_nonrandom+1)]
angle_repeat=[numpy.load("learningON/trial"+str(i)+"/angle_repeat.npy") for i in range(1, Ntrial_nonrandom+1)]
angle_random_novel=[numpy.load("learningOFF/trial"+str(i)+"/angle_novel.npy") for i in range(1, Ntrial_random+1)]
angle_random_repeat=[numpy.load("learningOFF/trial"+str(i)+"/angle_repeat.npy") for i in range(1, Ntrial_random+1)]

cutdata=lambda data, n: numpy.hstack([numpy.mean(x[n]) for x in data])
cutdata_random=lambda n: numpy.mean(numpy.hstack([cutdata(angle_random_novel,n), cutdata(angle_random_repeat,n)]))
angle_start_novel=cutdata(angle_novel, 0)
angle_start_repeat=cutdata(angle_repeat, 0)
angle_start_random=cutdata_random(0)
angle_run_novel=cutdata(angle_novel, 1)
angle_run_repeat=cutdata(angle_repeat, 1)
angle_run_random=cutdata_random(1)
angle_end_novel=cutdata(angle_novel, 2)
angle_end_repeat=cutdata(angle_repeat, 2)
angle_end_random=cutdata_random(2)

angle_start_novel-=angle_start_random
angle_start_repeat-=angle_start_random

angle_run_novel-=angle_run_random
angle_run_repeat-=angle_run_random

angle_end_novel-=angle_end_random
angle_end_repeat-=angle_end_random

#plot
pylab.close()
pylab.figure(figsize=(1.5,2))
pylab.plot([0], [numpy.mean(angle_start_repeat)], "o", color="black")
pylab.plot([0]*Ntrial_nonrandom, angle_start_repeat, ".",  color="gray")
pylab.plot([1], [numpy.mean(angle_run_repeat)], "o",  color="black")
pylab.plot([1]*Ntrial_nonrandom, angle_run_repeat,  ".", color="gray")
pylab.plot([2], [numpy.mean(angle_end_repeat)], "o",  color="black")
pylab.plot([2]*Ntrial_nonrandom, angle_end_repeat,  ".", color="gray")
pylab.xticks([0,1,2], ["Start","Run", "Goal"], rotation="vertical")
pylab.xlim([-0.5, 2.5])
pylab.ylabel("Mean angular displacement\n(baseline-subtracted)")
#pylab.yticks([-60,-30,0])
#pylab.ylim([-60,0])
pylab.tight_layout()
pylab.savefig("angle_diff_repeat.svg")

#plot
pylab.close()
pylab.figure(figsize=(1.5,2))
pylab.plot([0], [numpy.mean(angle_start_novel)], "o", color="black")
pylab.plot([0]*Ntrial_nonrandom, angle_start_novel, ".",  color="gray")
pylab.plot([1], [numpy.mean(angle_run_novel)], "o",  color="black")
pylab.plot([1]*Ntrial_nonrandom, angle_run_novel,  ".", color="gray")
pylab.plot([2], [numpy.mean(angle_end_novel)], "o",  color="black")
pylab.plot([2]*Ntrial_nonrandom, angle_end_novel,  ".", color="gray")
pylab.xticks([0,1,2], ["Start","Run", "Goal"], rotation="vertical")
pylab.xlim([-0.5, 2.5])
pylab.ylabel("Mean angular displacement\n(baseline-subtracted)")
#pylab.yticks([-60,-30,0])
#pylab.ylim([-60,0])
pylab.tight_layout()
pylab.savefig("angle_diff_novel.svg")

#statistical test
stattest_func=lambda x,y: scipy.stats.ttest_rel(x,y)
stat=numpy.zeros([6,2])
stat[0,:]=stattest_func(angle_start_repeat, angle_run_repeat)
stat[1,:]=stattest_func(angle_run_repeat, angle_end_repeat)
stat[2,:]=stattest_func(angle_end_repeat, angle_start_repeat)
stat[3,:]=stattest_func(angle_start_novel, angle_run_novel)
stat[4,:]=stattest_func(angle_run_novel, angle_end_novel)
stat[5,:]=stattest_func(angle_end_novel, angle_start_novel)
numpy.savetxt("angle_diff_stat_ttest_rel.csv", stat, delimiter=",")

stattest_func=lambda x: scipy.stats.shapiro(x)
stat=numpy.zeros([6,2])
stat[0,:]=stattest_func(angle_start_repeat)
stat[1,:]=stattest_func(angle_run_repeat)
stat[2,:]=stattest_func(angle_end_repeat)
stat[3,:]=stattest_func(angle_start_novel)
stat[4,:]=stattest_func(angle_run_novel)
stat[5,:]=stattest_func(angle_end_novel)
numpy.savetxt("angle_diff_stat_shapiro.csv", stat, delimiter=",")

