#!/bin/bash

#dataset="../../../datasets_200"
dataset="../../../datasets"
#dataset="../../../sample"
out="multimodal_melody_2.csv"
track_type="melody"
other_track_type="bass"
tresh=0.25

styles=(class jazz kar)

./multimodal_loo.py header > $out

for i in ${styles[@]}
do
    #echo $i
    echo "./multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i}"
    ./multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i} >> $out
    
done
