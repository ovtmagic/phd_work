#!/bin/bash

#dataset="sample"
dataset="../../../datasets"
out="icpram_6.3_melody.csv"

threshold="0.25"
track_type="melody"


# b_class_jazz.model	b_class_kar.model	b_jazz_kar.model

track_selection.py header > $out

echo $track_type $threshold arff/m_jazz_kar.model
track_selection.py $track_type $threshold arff/m_jazz_kar.model ${dataset}/class/class_train.csv ${dataset}/class/class >> $out

echo $track_type $threshold arff/m_class_kar.model 
track_selection.py $track_type $threshold arff/m_class_kar.model ${dataset}/jazz/jazz_train.csv ${dataset}/jazz/jazz >> $out

echo $track_type $threshold arff/m_class_jazz.model
track_selection.py $track_type $threshold arff/m_class_jazz.model ${dataset}/kar/kar_train.csv ${dataset}/kar/kar >> $out

