#!/usr/bin/env python3

import numpy

def calc_angle(rate, pos, pos_goal):
    centerX=numpy.zeros([xlen, ylen])
    centerY=numpy.zeros([xlen, ylen])
    for i in range(xlen):
        for j in range(ylen):
            centerX[i,j]=float(i)
            centerY[i,j]=float(j)
    centerX=centerX.reshape(xlen*ylen)
    centerY=centerY.reshape(xlen*ylen)

    ret=[]
    for t in range(rate.shape[0]):
        r=rate[t,:]
        p=pos[t,:]
        if numpy.max(r)<=0.01:
            continue
        activity_center=numpy.array([centerX@r, centerY@r])/numpy.sum(r)
        vecactivity=activity_center-p
        vecgoal=pos_goal-p
        norma=numpy.sqrt(vecactivity@vecactivity)
        normr=numpy.sqrt(vecgoal@vecgoal)
        if normr>0 and norma>1:
            angle=numpy.arccos((vecactivity@vecgoal)/norma/normr)/numpy.pi*180.0
            ret.append(angle)
    return numpy.array(ret)


#analyse data
xlen=50
ylen=50
startlen=3.0 #sec
#endlen=15.0 #sec

set_info=numpy.loadtxt("time_explore.csv", delimiter=",")

angle_start_novel=[]
angle_start_repeat=[]
angle_run_novel=[]
angle_run_repeat=[]
angle_end_novel=[]
angle_end_repeat=[]

for trial in range(1,21):
    print(trial)
    explore_time=set_info[trial-1, 1]
    if trial==1 or explore_time>=300:
        continue
    pos_start=set_info[trial-1, [2,3]]
    pos_reward=set_info[trial-1, [4,5]]
    rate_data=numpy.loadtxt("rate_set"+str(trial)+".csv", delimiter=",")
    pos_data=numpy.loadtxt("pos_set"+str(trial)+".csv", delimiter=",")
    time=rate_data[:,0]-rate_data[0,0]
    endtime=explore_time+startlen
    rate_data=rate_data[:,1:]
    pos_data=pos_data[:,1:]

    filtstart=(time<startlen)
    filtrun=(time>=startlen)*(time<=endtime)
    filtend=(time>endtime)
    filtpastpath=(time>=endtime-3)*(time<=endtime)
    pos_pastpath=numpy.mean(pos_data[filtpastpath,:], axis=0)
    if trial in [6,11,16]:
        angle_start_novel.append(calc_angle(rate_data[filtstart,:],pos_data[filtstart,:],pos_reward))
        angle_run_novel.append(calc_angle(rate_data[filtrun,:],pos_data[filtrun,:],pos_reward))
        angle_end_novel.append(calc_angle(rate_data[filtend,:],pos_data[filtend,:],pos_pastpath))
    else:
        angle_start_repeat.append(calc_angle(rate_data[filtstart,:],pos_data[filtstart,:],pos_reward))
        angle_run_repeat.append(calc_angle(rate_data[filtrun,:],pos_data[filtrun,:],pos_reward))
        angle_end_repeat.append(calc_angle(rate_data[filtend,:],pos_data[filtend,:],pos_pastpath))

angle_start_repeat=numpy.hstack(angle_start_repeat)
angle_start_novel=numpy.hstack(angle_start_novel)
angle_run_repeat=numpy.hstack(angle_run_repeat)
angle_run_novel=numpy.hstack(angle_run_novel)
angle_end_repeat=numpy.hstack(angle_end_repeat)
angle_end_novel=numpy.hstack(angle_end_novel)

numpy.save("angle_novel.npy", [angle_start_novel, angle_run_novel, angle_end_novel])
numpy.save("angle_repeat.npy", [angle_start_repeat, angle_run_repeat, angle_end_repeat])
