#!/usr/bin/env python3

import csv
import numpy

def norm_vec(vec):
    vec_sum=numpy.sqrt(numpy.sum(vec**2))
    if vec_sum>0:
        return vec/vec_sum
    else:
        return vec

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

def init_pos(reward_pos):
    mindist_start_reward=10.0
    ret=reward_pos+0.0
    while numpy.sum((ret-reward_pos)**2)<mindist_start_reward**2:
        ret[0]=(xmax-xmin)*numpy.random.rand()+xmin
        ret[1]=(ymax-ymin)*numpy.random.rand()+ymin
    return numpy.array(ret)

slope=1.0
threshold=2.0/1000.0
def ReLU(x):
    return numpy.maximum(slope*(x-threshold), 0.0)


#settings
time_pitch=1.0 #ms
save_pitch=20
xlen=50
ylen=50
margin=5
xmin=margin; ymin=margin; xmax=xlen-margin; ymax=ylen-margin

tauI=10.0 #ms
eta_nodopa=0.1
eta_dopa=0.1
eta=eta_nodopa
taudeltaW=10.0*1000.0 #ms

tauSTD=300.0 #ms
tauSTF=200.0 #ms
coefSTD=0.4

#weights
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
rate_hist=[]
pos_hist=[]

numpy.save("W_init.npy", W)

#place cell
noise_amp=0.05/1000.0
theta_amp=5.0/1000.0
PFrate_move=5.0/1000.0
PFrate_rest=1.0/1000.0
PFfreq_nodopa=1.0
PFfreq_dopa=1.0
Iextlen=int(200.0/time_pitch)
PFwidth=2.0

centerX=numpy.zeros([xlen, ylen])
centerY=numpy.zeros([xlen, ylen])
for i in range(xlen):
    for j in range(ylen):
        centerX[i,j]=float(i)
        centerY[i,j]=float(j)

#motion, reward, sequence
posreward_candidates=numpy.array([[0.3*xlen, 0.3*ylen], [0.7*xlen, 0.3*ylen], [0.3*xlen, 0.7*ylen], [0.7*xlen, 0.7*ylen]])
posreward_candidates=list(posreward_candidates[numpy.random.permutation(len(posreward_candidates)),:])
rewardarea=3.0
rewardreset=5
rewardnum=len(posreward_candidates)*rewardreset
max_time=300.0*1000.0 #ms

motion_speed=0.01
motion_noise=0.05*numpy.sqrt(time_pitch)
seq_to_motion=0.01

stop_len_start=3.0*1000.0
stop_len_reward=15.0*1000.0
SWRinterval=1000.0
SWRlen=800.0

#variables
moving=0
dopamine=0
rewardcount=0
pos_phase=0.0
Iext_sw=0
Iextinh_sw=0
setend_sw=0
time_stop=0.0
time_explore=0.0
time_explore_hist=[]

posreward=posreward_candidates.pop()
pos_start=init_pos(posreward)
pos=pos_start+0.0
activity_center=pos+0.0
vel=numpy.random.randn(2)
vel=norm_vec(vel)

#simulation
t=0
print("simulation start.",str(rewardnum),"trials.")
while True:
    t+=1
    time_ms=float(t)*time_pitch
    time_sec=time_ms/1000.0
    if time_ms%1000==0:
        print(time_sec, "sec", pos, vel)

    #terminate too long exploration
    if time_explore>max_time:
        print(str(time_sec), "sec Terminated trial", str(rewardcount+1), "/", str(rewardnum))
        dopamine=1; rewardcount+=1; time_stop=-1.0; setend_sw=1 #no reward time
        time_explore_hist.append([time_sec, time_explore/1000.0, pos_start[0], pos_start[1], posreward[0], posreward[1]])
    
    #reward -> restart
    if dopamine==0 and numpy.sum((pos-posreward)**2)<rewardarea**2: #reward found
        print(str(time_sec), "sec Goal trial", str(rewardcount+1), "/", str(rewardnum))
        dopamine=1; rewardcount+=1; time_stop=0.0
        time_explore_hist.append([time_sec, time_explore/1000.0, pos_start[0], pos_start[1], posreward[0], posreward[1]])
    elif dopamine==1 and time_stop<0: #restart
        if rewardcount%rewardreset==0:
            if len(posreward_candidates)==0: #finish simulation
                break
            posreward=posreward_candidates.pop()
            print("reset reward.")
        print(str(time_sec), "sec Start trial", str(rewardcount+1), "/", str(rewardnum))
        dopamine=0; time_stop=0.0; time_explore=0.0
        pos_start=init_pos(posreward)
        pos=pos_start+0.0

    #stop or move, sequence generation
    if time_stop>=0: #stop
        moving=0;
        #sequence generation
        if time_stop%SWRinterval>=0.0 and time_stop%SWRinterval<time_pitch:
            Iext_sw=Iextlen
        if time_stop%SWRinterval<SWRlen:
            Iextinh_sw=0
        else:
            Iextinh_sw=1
        time_stop+=time_pitch
        if dopamine==0 and time_stop>stop_len_start:
            time_stop=-1.0
        elif dopamine==1 and time_stop>stop_len_reward:
            time_stop=-1.0; setend_sw=1
    else: #move
        moving=1; Iext_sw=0; Iextinh_sw=0
        time_explore+=time_pitch
        pos=numpy.minimum(numpy.array([xmax,ymax]), numpy.maximum(numpy.array([xmin,ymin]), pos+time_pitch*motion_speed*vel))
        
    #external inputs
    if moving:
        Itheta=theta_amp*0.5*(numpy.sin(2.0*numpy.pi*time_ms/1000.0*7.0)+1.0)
        Iext=placefield_func(pos[0], pos[1], centerX, centerY, PFrate_move, PFwidth)
        Iextinh=0.0
    else:
        Itheta=0.0
        if dopamine:
            eta=eta_dopa
            if numpy.random.rand()<PFfreq_dopa:
                Iext_sw=Iextlen
        else:
            eta=eta_nodopa
            if numpy.random.rand()<PFfreq_nodopa:
                Iext_sw=Iextlen
        if Iext_sw>0:
            Iext=placefield_func(pos[0], pos[1], centerX, centerY, PFrate_rest, PFwidth)
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

    #update sequence vector and velocity
    rate_sum=numpy.sum(rate)
    if rate_sum>0:
        activity_center[0]=numpy.sum(centerX*rate)/rate_sum
        activity_center[1]=numpy.sum(centerY*rate)/rate_sum
        seq_vec=norm_vec(activity_center-pos)
    else:
        seq_vec=numpy.zeros(2)
    vel+=time_pitch*seq_to_motion*seq_vec+motion_noise*numpy.random.randn(2)
    vel=norm_vec(vel)

    #save results
    if t%save_pitch==0:
        temp=numpy.hstack([time_sec, rate.reshape(rate.size)])
        rate_hist.append(temp)
        #csv_rate.writerow(temp); f_rate.flush();
        temp=numpy.array([time_sec,pos[0],pos[1]])
        pos_hist.append(temp)
        #csv_pos.writerow(temp); f_pos.flush();
        
    if setend_sw==1:
        setend_sw=0
        numpy.savetxt("rate_set"+str(rewardcount)+".csv", numpy.array(rate_hist), delimiter=",")
        rate_hist=[]
        numpy.savetxt("pos_set"+str(rewardcount)+".csv", numpy.array(pos_hist), delimiter=",")
        pos_hist=[]
        numpy.save("W_set"+str(rewardcount)+".npy", W)
        numpy.savetxt("time_explore.csv", numpy.array(time_explore_hist), delimiter=",")

numpy.save("W_end.npy", W)
numpy.savetxt("time_explore.csv", numpy.array(time_explore_hist), delimiter=",")
