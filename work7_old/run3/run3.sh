#!/bin/bash

rm res3.csv

list=(kar jazz class)
type_list=(melody bass)

for track_type in ${type_list[@]}
do
    for i in ${list[@]}
    do
        echo $track_type , $i
        csv="datasets/${i}/${i}.csv"
        dataset="datasets/${i}/${i}"
        #echo $track_type $csv $dataset
        leave-one-out.py $track_type $csv $dataset >> res3.csv
    done
done
