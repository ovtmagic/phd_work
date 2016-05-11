#!/bin/bash



list=(class_900_0
class_900_1
class_900_2
class_900_3
class_900_4
class_900_5
class_900_6
class_900_7
class_900_8
class_900_9
class_900_10
)


rm res2.csv
for i in ${list[@]}
do
	echo $i
	leave-one-out.py melody ../csv/${i}.csv ../class_900 >>  res2.csv
done

for i in ${list[@]}
do
	echo $i
	leave-one-out.py bass ../csv/${i}.csv ../class_900 >>  res2.csv
done
