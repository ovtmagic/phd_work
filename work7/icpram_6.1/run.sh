#!/bin/bash

datasets="../../../datasets"
track_type="bass"
out="icpram_6.1.csv"

#statistics.py bass $datasets/all/all_test.csv $datasets/all/all

statistics.py bass ${datasets}_all/all_train.csv ${datasets}_all/all > ${track_type}_all_${out}


list=(class jazz kar)
for i in ${list[@]}
do
    echo ">>>>",${track_type}_${i}_${out}
    statistics.py bass $datasets/${i}/${i}_train.csv $datasets/${i}/${i} > ${track_type}_${i}_${out}
	

done
