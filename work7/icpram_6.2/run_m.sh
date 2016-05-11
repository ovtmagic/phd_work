#!/bin/bash

dataset="../icpram_6.4/sample/"
#dataset="../../../datasets"
out="x_icpram_6.2_melody.csv"
genres=(class jazz kar)
track_type="melody"
threshold="0.25"


leave-one-out.py header > $out

for i in ${genres[@]}
do
    echo $i $track_type $dataset/$i
    leave-one-out.py $track_type $threshold ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i} >> $out
done
