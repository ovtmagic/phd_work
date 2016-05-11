#!/bin/bash

#dataset="../../../sample"
dataset="../../../datasets_200"
out="icpram_6.2_200_bass.csv"
genres=(clas200 jazz200 kar200)
track_type="bass"
threshold="0.25"


leave-one-out.py header > $out

for i in ${genres[@]}
do
    echo $i $track_type $dataset/$i
    leave-one-out.py $track_type $threshold ${dataset}/${i}/${i}.csv ${dataset}/${i}/${i} >> $out
done
