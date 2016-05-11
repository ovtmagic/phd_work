#!/bin/bash

list=(kar jazz class)

for i in ${list[@]}
do 
	arff.py melody ../datasets/${i}/${i}.csv ../datasets/${i}/${i} > arff/m_${i}.arff
	arff.py melody ../datasets/${i}/${i}_test.csv ../datasets/${i}/${i} > arff/m_${i}_test.arff
	arff.py melody ../datasets/${i}/${i}_train.csv ../datasets/${i}/${i} > arff/m_${i}_train.arff
	arff.py bass ../datasets/${i}/${i}.csv ../datasets/${i}/${i} > arff/b_${i}.arff
	arff.py bass ../datasets/${i}/${i}_test.csv ../datasets/${i}/${i} > arff/b_${i}_test.arff
	arff.py bass ../datasets/${i}/${i}_train.csv ../datasets/${i}/${i} > arff/b_${i}_train.arff
done
