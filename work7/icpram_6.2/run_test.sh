#!/bin/bash

#------------------------------------------------
# Using train and test datasets
#------------------------------------------------

#dataset="/tmp/sample"
dataset="../../../datasets"
out="track_select_bass_test.csv"
track_type="bass"

tresh=0.25

# first letter
fl=`echo $track_type|cut -c 1`


echo $fl
styles=(class jazz kar)

track_selection.py header > $out

for i in ${styles[@]}
do
    #echo $i
    echo "track_selection.py $track_type $tresh ${dataset}/arff/${fl}_${i}_train.model ${dataset}/${i}/${i}_test.csv ${dataset}/${i}/${i}"
    track_selection.py $track_type $tresh ${dataset}/arff/${fl}_${i}_train.model ${dataset}/${i}/${i}_test.csv ${dataset}/${i}/${i} >> $out  
done
