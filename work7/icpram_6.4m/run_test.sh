#!/bin/bash

#------------------------------------------------
# Using train and test datasets
#------------------------------------------------

#dataset="../../../datasets_200"
dataset="../../../datasets"
out="multimodal_melody2.csv"
track_type="melody"
other_track_type="bass"
tresh=0.25

# bass and melody first letter
bfl=`echo $track_type|cut -c 1`
mfl=`echo $other_track_type|cut -c 1`

echo $bfl $mfl
styles=(class jazz kar)

multimodal.py header > $out

for i in ${styles[@]}
do
    #echo $i
    echo "multimodal.py $track_type $other_track_type $tresh ${dataset}/arff/${bfl}_${i}_train.model ${dataset}/arff/${mfl}_${i}_train.model ${dataset}/${i}/${i}_test.csv ${dataset}/${i}/${i}"
    multimodal.py $track_type $other_track_type $tresh ${dataset}/arff/${bfl}_${i}_train.model ${dataset}/arff/${mfl}_${i}_train.model ${dataset}/${i}/${i}_test.csv ${dataset}/${i}/${i} >> $out
done
