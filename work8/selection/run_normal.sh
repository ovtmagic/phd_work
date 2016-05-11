#!/bin/bash

#------------------------------------------------------------------------
#
# Seleccion de la pista de bajo/melodia sin RESAMPLE
#
#------------------------------------------------------------------------

#dataset="../../../sample"
dataset="../../../datasets"
genres=(class jazz kar)
threshold="0.25"

out="bass_selection_normal.csv"
track_type="bass"
# bass and melody first letter
bfl=`echo $track_type|cut -c 1`

track_selection.py header > $out

for i in ${genres[@]}
do
    echo $i $track_type $dataset/$i
    track_selection.py $track_type $threshold  ${dataset}/arff/${bfl}_${i}_train.model ${dataset}/${i}/${i}_test.csv ${dataset}/${i}/${i} >> $out
done
