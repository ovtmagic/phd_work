#!/bin/bash


list=(class_900_0
class_900_1
class_900_10
class_900_2
class_900_3
class_900_4
class_900_5
class_900_6
class_900_7
class_900_8
class_900_9)

for i in ${list[@]}
do
    echo $i
    ../get_prob_and_tags.py ../m_train.arff ../b_train.arff $i/$i.csv $i/$i > to_check_all/$i.check
    ../get_prob_and_tags2.py ../m_train.arff ../b_train.arff $i/$i.csv $i/$i > to_check/$i.check
done