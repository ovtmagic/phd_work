#!/bin/bash


datasets="../../datasets"
styles=(class jazz kar)

track_type="bass"
for i in ${styles[@]}
do
    echo "Style (" $track_type "): " $i
    ./statistics.py ${track_type}  $datasets/${i}/${i}_train.csv $datasets/${i}/${i}
done

track_type="melody"
for i in ${styles[@]}
do
    echo "Style (" $track_type "): " $i
    ./statistics.py ${track_type}  $datasets/${i}/${i}_train.csv $datasets/${i}/${i}
done
    
    