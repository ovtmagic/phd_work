#!/bin/bash

arff_path="../arff/"
dataset="../../../datasets/"
#dataset="./sample/"
out=$1.csv
track_type=$1
tresh=0.25

fl=`echo $track_type|cut -c1`
genres=( class jazz kar )
filters=( "" "resample_" "smote_" "sss_" )


track_selection.py header > $out
for g in ${genres[@]}
do
    for f in "${filters[@]}"
    do
        trainfile="${arff_path}${f}${fl}_${g}_train.model"
        echo $trainfile
        track_selection.py $track_type $tresh $trainfile "$dataset/$g/${g}_test.csv" "$dataset/$g/$g" >> $out
        
    done


done
