#!/usr/bin/env python3

import csv
import numpy

def placefield_func(X, Y, centerX, centerY, max_rate, width):
    return max_rate*numpy.exp(-0.5*(X-centerX)**2/width**2-0.5*(Y-centerY)**2/width**2)

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

slope=1.0
threshold=2.0/1000.0
def ReLU(x):
    return numpy.maximum(slope*(x-threshold), 0.0)

#parameters
time_pitch=1.0 #ms
save_pitch=10
simlen_sec=30.0
simlen=int(simlen_sec*1000.0/time_pitch)
xlen=50
ylen=50

tauI=10.0 #ms
eta=0.5
taudeltaW=10.0*1000.0 #ms

tauSTD=300.0 #ms
tauSTF=200.0 #ms
coefSTD=0.4

winh=5e-4

Wmin=0.0
Wsum=1.0
Wsuminit=1.0

synapse_arr=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
synapse_num=len(synapse_arr)

W=numpy.zeros([synapse_num, xlen, ylen])
deltaW=numpy.zeros([synapse_num, xlen, ylen])
for i in range(xlen):
    for j in range(ylen):
        temp=numpy.random.rand(synapse_num)
        W[:,i,j]=Wsuminit*temp/numpy.sum(temp)

I=numpy.zeros([xlen,ylen])
STD=numpy.ones_like(I)
STF=coefSTD*numpy.ones_like(I)
Iinh=0.0

#save
f_rate=open("rate.csv", "w")
csv_rate=csv.writer(f_rate, delimiter=",")
f_pos=open("pos.csv", "w")
csv_pos=csv.writer(f_pos, delimiter=",")

numpy.save("W_init.npy", W)

#place cell
noise_amp=0.05/1000.0
theta_amp=5.0/1000.0
PFrate_move=5.0/1000.0
PFrate_rest=1.0/1000.0
PFfreq_nodopa=0.1/1000.0
PFfreq_dopa=1.0
PFlen=int(200.0/time_pitch)
PFwidth=2.0

centerX=numpy.zeros([xlen, ylen])
centerY=numpy.zeros([xlen, ylen])
for i in range(xlen):
    for j in range(ylen):
        centerX[i,j]=float(i)
        centerY[i,j]=float(j)

posreward=[0.5*float(xlen), 0.5*float(ylen)]

set_len=10*1000.0
SWRinterval=1000.0
SWRlen=800.0

moving=0
dopamine=0
pos_phase=0.0
Iext_sw=0
Iextinh_sw=0
for t in range(simlen):
    time_ms=float(t)*time_pitch
    if time_ms%1000==0:
        print(time_ms/1000,"sec")

    #for sequence generation
    if time_ms%SWRinterval>=0.0 and time_ms%SWRinterval<0.0+time_pitch:
        Iext_sw=PFlen
    if time_ms%SWRinterval<SWRlen:
        Iextinh_sw=0
    else:
        Iextinh_sw=1

    #position
    time_set=time_ms%set_len
    x=25.0
    y=25.0
    moving=0
    dopamine=1

    #external inputs
    if moving:
        Itheta=theta_amp*0.5*(numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)+1.0)
        Iext=placefield_func(x, y, centerX, centerY, PFrate_move, PFwidth)
        Iextinh=0.0
    else:
        Itheta=0.0
        if dopamine:
            if numpy.random.rand()<PFfreq_dopa:
                Iext_sw=PFlen
        else:
            if numpy.random.rand()<PFfreq_nodopa:
                Iext_sw=PFlen
        if Iext_sw>0:
            Iext=placefield_func(x, y, centerX, centerY, PFrate_rest, PFwidth)
            Iext_sw=Iext_sw-1
        else:
            Iext=0.0
        #inhibition
        if Iextinh_sw>0:
            Iextinh=0.1
        else:
            Iextinh=0.0
            
    #recurrent transmission
    rate=ReLU(I)
    rate_out=rate*STD*STF
    Isyn=numpy.zeros_like(rate)
    for i in range(synapse_num):
        Isyn=Isyn+W[i,:,:]*shift2D(rate_out,synapse_arr[i][0],synapse_arr[i][1])
    
    #dynamics
    I=I+time_pitch*(-I/tauI+Isyn-Iinh+Iext-Iextinh-Itheta)+noise_amp*numpy.sqrt(time_pitch)*numpy.random.randn(xlen,ylen)
    Iinh=Iinh+time_pitch*(-Iinh/tauI+winh*numpy.sum(rate_out))
    STD=STD+time_pitch*((1.0-STD)/tauSTD-rate_out)
    STF=STF+time_pitch*((coefSTD-STF)/tauSTF+coefSTD*rate*(1.0-STF))

    #Hebb
    rate=ReLU(I)
    W=W+time_pitch*deltaW
    for i in range(synapse_num):
        deltaW[i,:,:]=deltaW[i,:,:]+time_pitch*(-deltaW[i,:,:]+eta*rate*shift2D(rate_out,synapse_arr[i][0],synapse_arr[i][1]))/taudeltaW #Hebb
    #normalization
    W[W<Wmin]=Wmin
    temp=numpy.repeat(numpy.sum(W, axis=0, keepdims=True), synapse_num, axis=0)
    W=numpy.select([temp<=Wsum, temp>Wsum], [W, Wsum*W/temp])

    #save results
    if t%save_pitch==0:
        temp=numpy.hstack([time_ms/1000.0, rate.reshape(rate.size)])
        csv_rate.writerow(temp); f_rate.flush();
        csv_pos.writerow(numpy.array([time_ms/1000.0,x,y])); f_pos.flush();
        
    if t!=0 and (time_ms/1000.0)%int(set_len/1000.0)==0:
        temp=int(time_ms/1000.0)
        numpy.save("W_"+str(temp)+"s.npy", W)

numpy.save("W_end.npy", W)
