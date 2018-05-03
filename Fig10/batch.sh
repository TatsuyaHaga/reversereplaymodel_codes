#!/bin/bash

N_ON=10
N_OFF=10

cd learningON/
for N in `seq 1 $N_ON`
do
    DIR=trial$N
    cp -r src_learningON/ $DIR
    cd $DIR
    pwd
    bash exec.sh
    cd ../
done
cd ../

cd learningOFF/
for N in `seq 1 $N_OFF`
do
    DIR=trial$N
    cp -r src_learningOFF/ $DIR
    cd $DIR
    pwd
    bash exec.sh
    cd ../
done
cd ../

bash batch_aftersim.sh
