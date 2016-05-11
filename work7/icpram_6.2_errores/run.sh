#!/bin/bash

#dataset="../../../sample"
dataset="../../../datasets"
out="icpram_6.2_bass.csv"
genres=(class)
track_type="bass"
threshold="0.25"


leave-one-out.py header > $out

for i in ${genres[@]}
do
    echo $i $track_type $dataset/$i
    ./leave-one-out.py $track_type $threshold ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i}  >> $out
done
