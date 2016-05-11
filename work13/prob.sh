#!/bin/bash


datasets="../../datasets"
#datasets="sample"
styles=(class jazz kar)
ext="txt"

for i in ${styles[@]}
do
	echo $i
	echo "./get_prob_and_tags2_loo.py ${datasets}/${i}/${i}_train.csv ${datasets}/${i}/${i}"
	#./get_prob_and_tags2_loo.py ${datasets}/${i}/${i}_train.csv ${datasets}/${i}/${i} > prob/prob_${i}_train.${ext}
	./get_prob_and_tags2_loo.py ${datasets}/${i}/${i}.csv ${datasets}/${i}/${i} > prob/prob_${i}.${ext}
done

