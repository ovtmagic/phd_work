#!/bin/bash

#------------------------------------------------
# Using train and leave one out
#------------------------------------------------

dataset="../../../../datasets"
#dataset="sample2"

track_type="$1"

out="${track_type}_s.txt"
echo $out
tresh=0.25

styles=(class jazz kar)
#styles=(class)

./leave-one-out.py header > $out

for i in ${styles[@]}
do
    echo ">>>>" $i
    echo "./leave-one-out.py $track_type $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i}"
    ./leave-one-out.py $track_type $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i} >> $out
done
