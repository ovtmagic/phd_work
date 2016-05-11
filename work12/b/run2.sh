#!/bin/bash

#------------------------------------------------
# Using train and leave one out
#------------------------------------------------

dataset="../../../datasets"
#dataset="/tmp/sample"
out="bass2.csv"
track_type="bass"
other_track_type1="melody"
other_track_type2="accomp"
tresh=0.25

styles=(class jazz kar)


multimodal_loo2.py header > $out

for i in ${styles[@]}
do
    echo ">>>>" $i
    echo "multimodal_loo2.py $track_type $other_track_type1 $other_track_type2 $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i}"
    multimodal_loo2.py $track_type $other_track_type1 $other_track_type2 $tresh ${dataset}/${i}/${i}_train.csv ${dataset}/${i}/${i} >> $out
done
