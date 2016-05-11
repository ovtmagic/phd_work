#!/bin/bash

list=(kar jazz class)



for i in ${list[@]}
do
    echo $i
    model.sh arff/m_${i}.arff arff/m_${i}.model
    model.sh arff/b_${i}.arff arff/b_${i}.model
    model.sh arff/a_${i}.arff arff/a_${i}.model
    model.sh arff/m_${i}_train.arff arff/m_${i}_train.model
    model.sh arff/b_${i}_train.arff arff/b_${i}_train.model
    model.sh arff/a_${i}_train.arff arff/a_${i}_train.model
done
