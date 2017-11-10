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
simlen_sec=150.0
simlen=int(simlen_sec*1000.0/time_pitch)
xlen=50
ylen=50

tauI=10.0 #ms
eta=1.0
taudeltaW=30.0*1000.0 #ms

tauSTD=300.0 #ms
tauSTF=200.0 #ms
coefSTD=0.4

winh=5e-4

Wmin=0.0
Wsum=1.0
Wsuminit=0.5

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
f_rate1D=open("rate1D.csv", "w")
csv_rate1D=csv.writer(f_rate1D, delimiter=",")
f_pos1D=open("pos1D.csv", "w")
csv_pos1D=csv.writer(f_pos1D, delimiter=",")

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

posA=[0.5*float(xlen), 0.3*float(ylen)]
posB=[0.5*float(xlen), 0.7*float(ylen)]
posC1=[0.9*float(xlen), 0.7*float(ylen)]
posD1=[0.9*float(xlen), 0.3*float(ylen)]
posC2=[0.1*float(xlen), 0.7*float(ylen)]
posD2=[0.1*float(xlen), 0.3*float(ylen)]

time1=2000.0
time2=4000.0
time3=6000.0
time4=8000.0
set_len=15000.0

direction=-1
moving=0
dopamine=0
pos_phase=0.0
Iext_sw=0
for t in range(simlen):
    time_ms=float(t)*time_pitch
    if time_ms%1000==0:
        print(time_ms/1000,"sec")

    if time_ms%set_len<time_pitch:
        direction=-direction
        if direction==1:
            posC=posC1
            posD=posD1
        else:
            posC=posC2
            posD=posD2
            
    #for prospective sequence
    if time_ms%set_len>=1000.0 and time_ms%set_len<1000.0+time_pitch:
        Iext_sw=PFlen

    #position
    time_set=time_ms%set_len
    if time_set<=time1:
        pos_phase=0.0
        x=posA[0]
        y=posA[1]
        moving=0
        dopamine=0
    elif time_set<=time2:
        pos_phase=(time_set-time1)/(time2-time1)
        x=posA[0]+(posB[0]-posA[0])*pos_phase
        y=posA[1]+(posB[1]-posA[1])*pos_phase
        moving=1
        dopamine=0
    elif time_set<=time3:
        pos_phase=(time_set-time2)/(time3-time2)
        x=posB[0]+(posC[0]-posB[0])*pos_phase
        y=posB[1]+(posC[1]-posB[1])*pos_phase
        pos_phase=pos_phase+1.0+(1.0-direction)
        moving=1
        dopamine=0
    elif time_set<=time4:
        pos_phase=(time_set-time3)/(time4-time3)
        x=posC[0]+(posD[0]-posC[0])*pos_phase
        y=posC[1]+(posD[1]-posC[1])*pos_phase
        pos_phase=pos_phase+2.0+(1.0-direction)
        moving=1
        dopamine=0
    elif time_set<=set_len:
        x=posD[0]
        y=posD[1]
        pos_phase=3.0+(1.0-direction)
        moving=0
        dopamine=0#(1-direction)/2 #reward OFF

    #external inputs
    if moving:
        Itheta=theta_amp*0.5*(numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)+1.0)
        Iext=placefield_func(x, y, centerX, centerY, PFrate_move, PFwidth)
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
    
    #recurrent transmission
    rate=ReLU(I)
    rate_out=rate*STD*STF
    Isyn=numpy.zeros_like(rate)
    for i in range(synapse_num):
        Isyn=Isyn+W[i,:,:]*shift2D(rate_out,synapse_arr[i][0],synapse_arr[i][1])
    
    #dynamics
    I=I+time_pitch*(-I/tauI+Isyn-Iinh+Iext-Itheta)+noise_amp*numpy.sqrt(time_pitch)*numpy.random.randn(xlen,ylen)
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
        #1-dim position
        temp=numpy.hstack([time_ms/1000.0, \
                           rate[int(posA[0]), int(posA[1]):int(posB[1])], \
                           rate[int(posB[0]):int(posC1[0]), int(posB[1])], \
                           rate[int(posC1[0]), int(posC1[1]):int(posD1[1]):-1], \
                           rate[int(posB[0]):int(posC2[0]):-1, int(posB[1])], \
                           rate[int(posC2[0]), int(posC2[1]):int(posD2[1]):-1] \
        ])
        csv_rate1D.writerow(temp); f_rate1D.flush();
        csv_pos1D.writerow(numpy.array([time_ms/1000.0,pos_phase])); f_pos1D.flush()
        
    if t!=0 and (time_ms/1000.0)%int(set_len/1000)==0:
        temp=int(time_ms/1000.0)
        numpy.save("W_"+str(temp)+"s.npy", W)

numpy.save("W_end.npy", W)
