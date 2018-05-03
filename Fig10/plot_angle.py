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
angle_random=[numpy.load("learningOFF/trial"+str(i)+"/angle_repeat.npy") for i in range(1, Ntrial_random+1)]

cutdata=lambda data, n: numpy.hstack([x[n] for x in data])
angle_start_novel=cutdata(angle_novel, 0)
angle_start_repeat=cutdata(angle_repeat, 0)
angle_start_random=cutdata(angle_random, 0)
angle_run_novel=cutdata(angle_novel, 1)
angle_run_repeat=cutdata(angle_repeat, 1)
angle_run_random=cutdata(angle_random, 1)
angle_end_novel=cutdata(angle_novel, 2)
angle_end_repeat=cutdata(angle_repeat, 2)
angle_end_random=cutdata(angle_random,2)

#plot
hist_range=[0,180]
xtick=[0,90,180]
Nbin=18

pylab.close()
pylab.figure(figsize=(2.5,1.5))
ymax=0.035
seaborn.distplot(angle_start_novel, bins=Nbin, kde=False, norm_hist=True, label="SWITCH", color="blue", hist_kws={"range": hist_range})
seaborn.distplot(angle_start_repeat, bins=Nbin, kde=False, norm_hist=True, label="REPEAT", color="green", hist_kws={"range": hist_range})
#seaborn.distplot(angle_start_random, bins=Nbin, kde=False, norm_hist=True, label="NOLEARN", color="red", hist_kws={"range": hist_range})
pylab.plot([numpy.mean(angle_start_novel)]*2, [0,ymax], color="blue")
pylab.plot([numpy.mean(angle_start_repeat)]*2, [0,ymax], color="green")
#pylab.plot([numpy.mean(angle_start_random)]*2, [0,ymax], color="red")
pylab.xlabel("Angular displacement [degree]")
pylab.ylabel("Probability")
pylab.xticks(xtick)
pylab.yticks([])
pylab.ylim([0,ymax])
pylab.legend()
pylab.tight_layout()
pylab.savefig("angle_start.svg")

pylab.close()
pylab.figure(figsize=(2.5,1.5))
ymax=0.02
seaborn.distplot(angle_run_novel, bins=Nbin, kde=False, norm_hist=True, label="SWITCH", color="blue", hist_kws={"range": hist_range})
seaborn.distplot(angle_run_repeat, bins=Nbin, kde=False, norm_hist=True, label="REPEAT", color="green", hist_kws={"range": hist_range})
#seaborn.distplot(angle_run_random, bins=Nbin, kde=False, norm_hist=True, label="NOLEARN", color="red", hist_kws={"range": hist_range})
pylab.plot([numpy.mean(angle_run_novel)]*2, [0,ymax], color="blue")
pylab.plot([numpy.mean(angle_run_repeat)]*2, [0,ymax], color="green")
#pylab.plot([numpy.mean(angle_run_random)]*2, [0,ymax], color="red")
pylab.xlabel("Angular displacement [degree]")
pylab.ylabel("Probability")
pylab.xticks(xtick)
pylab.yticks([])
pylab.ylim([0,ymax])
pylab.legend()
pylab.tight_layout()
pylab.savefig("angle_run.svg")

pylab.close()
pylab.figure(figsize=(2.5,1.5))
ymax=0.025
seaborn.distplot(angle_end_novel, bins=Nbin, kde=False, norm_hist=True, label="SWITCH", color="blue", hist_kws={"range": hist_range})
seaborn.distplot(angle_end_repeat, bins=Nbin, kde=False, norm_hist=True, label="REPEAT", color="green", hist_kws={"range": hist_range})
#seaborn.distplot(angle_end_random, bins=Nbin, kde=False, norm_hist=True, label="NOLEARN", color="red", hist_kws={"range": hist_range})
pylab.plot([numpy.mean(angle_end_novel)]*2, [0,ymax], color="blue")
pylab.plot([numpy.mean(angle_end_repeat)]*2, [0,ymax], color="green")
#pylab.plot([numpy.mean(angle_end_random)]*2, [0,ymax], color="red")
pylab.xlabel("Angular displacement [degree]")
pylab.ylabel("Probability")
pylab.xticks(xtick)
pylab.yticks([])
pylab.ylim([0,ymax])
pylab.legend()
pylab.tight_layout()
pylab.savefig("angle_end.svg")


#statistical test
stattest_func=scipy.stats.ranksums
stat=numpy.zeros([9,2])
stat[0,:]=stattest_func(angle_start_novel, angle_start_repeat)
stat[1,:]=stattest_func(angle_start_repeat, angle_start_random)
stat[2,:]=stattest_func(angle_start_novel, angle_start_random)
stat[3,:]=stattest_func(angle_run_novel, angle_run_repeat)
stat[4,:]=stattest_func(angle_run_repeat, angle_run_random)
stat[5,:]=stattest_func(angle_run_novel, angle_run_random)
stat[6,:]=stattest_func(angle_end_novel, angle_end_repeat)
stat[7,:]=stattest_func(angle_end_repeat, angle_end_random)
stat[8,:]=stattest_func(angle_end_novel, angle_end_random)
numpy.savetxt("angle_stat_ranksum.csv", stat, delimiter=",")

