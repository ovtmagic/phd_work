#!/bin/bash

#------------------------------------------------
# Using train and leave one out
#------------------------------------------------

dataset="../../../../datasets"
#dataset="./sample2"

track_type="$1"
other_track_type1="$2"
out="${track_type}_mm.txt"
tresh=0.25

styles=(class jazz kar)
#styles=(class)

./multimodal_loo.py header > $out

for i in ${styles[@]}
do
    echo ">>>>" $i
    echo "./multimodal_loo.py $track_type $other_track_type1 $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i}"
    ./multimodal_loo.py $track_type $other_track_type1 $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i} >> $out
done
