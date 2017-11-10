#!/usr/bin/env python3

import sys
import numpy
import scipy.stats
import multiprocessing

def STDP(post, pre, spike_time, release, STDPtype, STDPcombi):
    #symmetric
    STDPmax=1.0
    STDPtau=70.0 #ms
    #asymmetric: Bi and Poo,2001
    STDPmax_plus=0.777
    STDPmax_minus=0.273
    STDPtau_plus=16.8 #ms
    STDPtau_minus=33.7 #ms

    ret=0.0
    for j in range(spike_time.shape[1]):
        dif=spike_time[post,:]-spike_time[pre,j]
        #symmetric
        if STDPtype=="symmetric" and STDPcombi=="alltoall":
            ret=ret+STDPmax*release[pre,j]*numpy.sum(numpy.exp(-0.5*(dif/STDPtau)**2.0))
        elif STDPtype=="symmetric" and STDPcombi=="nearest":
            dif_plus=dif>=0.0
            dif_minus=dif<0.0
            if numpy.any(dif_plus):
                ret=ret+STDPmax*release[pre,j]*numpy.exp(-0.5*(numpy.min(numpy.abs(dif[dif_plus]))/STDPtau)**2.0)
            if numpy.any(dif_minus):
                ret=ret+STDPmax*release[pre,j]*numpy.exp(-0.5*(numpy.min(numpy.abs(dif[dif_minus]))/STDPtau)**2.0)
        #Hebbian
        elif STDPtype=="hebb" and STDPcombi=="alltoall":
            dif_plus=dif>=0.0
            dif_minus=dif<0.0
            if numpy.any(dif_plus):
                ret=ret+STDPmax_plus*release[pre,j]*numpy.sum(numpy.exp(-numpy.abs(dif[dif_plus])/STDPtau_plus))
            if numpy.any(dif_minus):
                ret=ret-STDPmax_minus*release[pre,j]*numpy.sum(numpy.exp(-numpy.abs(dif[dif_minus])/STDPtau_minus))
        elif STDPtype=="hebb" and STDPcombi=="nearest":
            dif_plus=dif>=0.0
            dif_minus=dif<0.0
            if numpy.any(dif_plus):
                ret=ret+STDPmax_plus*release[pre,j]*numpy.exp(-numpy.min(numpy.abs(dif[dif_plus]))/STDPtau_plus)
            if numpy.any(dif_minus):
                ret=ret-STDPmax_minus*release[pre,j]*numpy.exp(-numpy.min(numpy.abs(dif[dif_minus]))/STDPtau_minus)
        #anti-Hebbian
        elif STDPtype=="anti" and STDPcombi=="alltoall":
            dif_plus=dif<0.0
            dif_minus=dif>=0.0
            if numpy.any(dif_plus):
                ret=ret+STDPmax_plus*release[pre,j]*numpy.sum(numpy.exp(-numpy.abs(dif[dif_plus])/STDPtau_plus))
            if numpy.any(dif_minus):
                ret=ret-STDPmax_minus*release[pre,j]*numpy.sum(numpy.exp(-numpy.abs(dif[dif_minus])/STDPtau_minus))
        elif STDPtype=="anti" and STDPcombi=="nearest":
            dif_plus=dif<0.0
            dif_minus=dif>=0.0
            if numpy.any(dif_plus):
                ret=ret+STDPmax_plus*release[pre,j]*numpy.exp(-numpy.min(numpy.abs(dif[dif_plus]))/STDPtau_plus)
            if numpy.any(dif_minus):
                ret=ret-STDPmax_minus*release[pre,j]*numpy.exp(-numpy.min(numpy.abs(dif[dif_minus]))/STDPtau_minus)
                
    return ret

#function for multiprocessing
def sample_eval(q, rand_seed, sample_in_process, spike_num, STDPtype, STDPcombi):
    #set seed
    numpy.random.seed(seed=rand_seed)
    
    #spike train parameters
    ref_period=1.0 #ms

    #short-term plasticity parameters
    STDsw=True
    STFsw=True

    #evaluate bias
    sample_num=100
    bias_len=10
    neuron_num=2*bias_len+1

    bias_hist=numpy.zeros([sample_in_process, 8])
    for nsamp in range(sample_in_process):
        #random parameters
        U=0.1+0.5*numpy.random.rand()
        tauSTD=50+550*numpy.random.rand() #ms
        tauSTF=10+290*numpy.random.rand() #ms
        deltaw_bias=numpy.zeros(sample_num)
        for s in range(sample_num):
            #generate spike train
            meanISI=5.0+15.0*numpy.random.rand()
            ms_per_neuron=5.0+15.0*numpy.random.rand()
            spike_time=numpy.zeros([neuron_num, spike_num])
            for n in range(neuron_num):
                spike_time[n][0]=ms_per_neuron*n
                for j in range(1,spike_num):
                    while spike_time[n][j]<spike_time[n][j-1]+ref_period:
                        spike_time[n][j]=spike_time[n][j-1]+numpy.random.exponential(meanISI)

            #simulate short-term plasticity
            release=numpy.ones([neuron_num, spike_num])
            if STDsw:
                for n in range(neuron_num):
                    STD=1.0
                    STF=U+0.0
                    for i in range(spike_num):
                        if STFsw:
                            release[n,i]=STD*STF
                            STD=STD-STF*STD
                            STF=STF+U*(1.0-STF)
                        else:
                            release[n,i]=STD
                            STD=STD-U*STD
                        #recovery
                        if i<spike_num-1:
                            STD=1.0-(1.0-STD)*numpy.exp(-(spike_time[n,i+1]-spike_time[n,i])/tauSTD)
                            if STFsw:
                                STF=U-(U-STF)*numpy.exp(-(spike_time[n,i+1]-spike_time[n,i])/tauSTF)

            #simulate STDP
            deltaw=numpy.zeros(neuron_num)
            for n in range(neuron_num): #post
                if n!=bias_len:
                    deltaw[n]=STDP(n, bias_len, spike_time, release, STDPtype, STDPcombi)
            deltaw_bias[s]=numpy.sum(deltaw[:bias_len])-numpy.sum(deltaw[bias_len+1:])

        wilcox=scipy.stats.wilcoxon(deltaw_bias, zero_method="wilcox")
        binom=scipy.stats.binom_test(len(deltaw_bias[deltaw_bias>0.0]), len(deltaw_bias), p=0.5, alternative="two-sided")
        bias_hist[nsamp,:]=[U, tauSTD, tauSTF, numpy.mean(deltaw_bias), wilcox[0], wilcox[1], len(deltaw_bias[deltaw_bias>0.0])/len(deltaw_bias), binom]
    
    q.put(bias_hist)


    
#main process
if __name__=="__main__":
    #setting
    spike_num=int(sys.argv[1])
    STDPtype=sys.argv[2] #"hebb" "symmetric" "anti"
    STDPcombi=sys.argv[3] #"alltoall" "nearest"
    sample_per_process=int(sys.argv[4])
    process_num=int(sys.argv[5])

    que=multiprocessing.Queue()

    process_arr=[]
    for i in range(process_num):
        process_arr.append(multiprocessing.Process(target=sample_eval, args=(que, i, sample_per_process, spike_num, STDPtype, STDPcombi)))
        process_arr[i].start()

    results=[]
    for i in range(process_num):
        results.append(que.get())

    for i in range(process_num):
        process_arr[i].join()

    results=numpy.vstack(results)
    numpy.savetxt("bias_log.csv", results, delimiter=",")
