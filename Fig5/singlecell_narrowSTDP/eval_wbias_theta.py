#!/usr/bin/env python3

import numpy
import scipy.stats

def symmetricSTDP(t_post, t_pre, release):
    STDPmax=1.0
    STDPtau=10.0 #ms
    return STDPmax*release*numpy.sum(numpy.exp(-0.5*((t_post-t_pre)/STDPtau)**2.0))

def gauss(x, sigma):
    return numpy.exp(-0.5*(x/sigma)**2)/numpy.sqrt(2.0*numpy.pi)/sigma

def vonmises(x,beta):
    return numpy.exp(beta*numpy.cos(x))*0.5/numpy.pi/scipy.special.i0(beta)

def gen_spiketrain(PFmax, PFwidth, phase_width):
    theta_phase_init=2.0*numpy.pi*numpy.random.rand()
    spike=[]
    for i in range(neuron_num):
        spike.append([])
    for t in range(simlen):
        pos=float(t)/float(simlen)
        theta_phase=2.0*numpy.pi*pos*8.0+theta_phase_init
        precess=numpy.pi*(PFcenter-pos)
        rate=PFmax*gauss(pos-PFcenter,PFwidth)*vonmises(theta_phase-precess,phase_width)
        for i in range(neuron_num):
            if numpy.random.rand()<rate[i]:
                spike[i].append(t)
    return spike

def simulate_plasticity(spike_time):
    U=0.37
    tauSTD=150.0 #ms
    tauSTF=40.0 #ms

    #simulate short-term plasticity
    release=[]
    for n in range(neuron_num):
        release.append([])
        STD=1.0
        STF=U+0.0
        for i in range(len(spike_time[n])):
            #recovery
            if i>0:
                STD=1.0-(1.0-STD)*numpy.exp(-(spike_time[n][i]-spike_time[n][i-1])/tauSTD)
                STF=U-(U-STF)*numpy.exp(-(spike_time[n][i]-spike_time[n][i-1])/tauSTF)
            #release
            release[n].append(STD*STF)
            STD=STD-STF*STD
            STF=STF+U*(1.0-STF)
            
    #simulate STDP
    deltaw=numpy.zeros(neuron_num)
    for j in range(len(spike_time[bias_len])): #pre
        for n in range(neuron_num): #post
            if n!=bias_len:
                for i in range(len(spike_time[n])):
                    deltaw[n]+=symmetricSTDP(spike_time[n][i], spike_time[bias_len][j], release[bias_len][j])
                    
    return numpy.sum(deltaw[:bias_len])-numpy.sum(deltaw[bias_len+1:])

def stat_test(deltaw_bias):
    wilcox=scipy.stats.wilcoxon(deltaw_bias, zero_method="wilcox")
    binom=scipy.stats.binom_test(len(deltaw_bias[deltaw_bias>0.0]), len(deltaw_bias), p=0.5, alternative="two-sided")
    return [numpy.mean(deltaw_bias), wilcox[0], wilcox[1], len(deltaw_bias[deltaw_bias>0.0])/len(deltaw_bias), binom]

    
neuron_num=81
bias_len=40
simlen=1000 #ms
PFcenter=2.0*numpy.arange(neuron_num)/float(neuron_num-1)-0.5
Nparam=1000
Nsample=100
PFwidth=0.2
rate_sigma=50.0
rate_time=numpy.arange(simlen)

results=numpy.zeros([Nparam, 7])
for p in range(Nparam):
    print(p+1)
    PFmax=0.14*numpy.random.rand()+0.01 #kHz
    phase_width=9.9*numpy.random.rand()+0.1
    deltaw_bias=numpy.zeros(Nsample)
    meanrate=numpy.zeros(simlen)
    for s in range(Nsample):
        spike=gen_spiketrain(PFmax, PFwidth, phase_width)
        deltaw_bias[s]=simulate_plasticity(spike)
        for tspike in spike[bias_len]:
            meanrate+=gauss(rate_time-tspike, rate_sigma)/float(Nsample)
        #meanrate+=len(spike[bias_len])/float(Nsample)
    results[p,:]=numpy.hstack([[numpy.max(meanrate), phase_width], stat_test(deltaw_bias)])

numpy.savetxt("bias_log.csv", results, delimiter=",")
