#!/bin/bash

dataset="sample"
out="multimodal_loo_sample.csv"
track_type="bass"
other_track_type="melody"
tresh=0.25

styles=(class jazz kar)

./multimodal_loo.py header > $out

for i in ${styles[@]}
do
    #echo $i
    echo "./multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}.csv ${dataset}/${i}/${i}"
    ./multimodal_loo.py $track_type $other_track_type $tresh ${dataset}/${i}/${i}.csv ${dataset}/${i}/${i} 
done
