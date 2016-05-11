#!/bin/bash

dataset="../../../datasets_200"
#dataset="../../../sample"
out="multimodal_bass_200.csv"
track_type="bass"
other_track_type="melody"
tresh=0.25

styles=(clas200 jazz200 kar200)

multimodal_loo.py header > $out

for i in ${styles[@]}
do
    #echo $i
    echo "./multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i}"
    #./multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i} >> $out
    multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}.csv ${dataset}/${i}/${i} >> $out
done
