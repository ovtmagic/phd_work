#!/bin/bash


list=(class_900_0
class_900_1
class_900_2
class_900_3
class_900_4
class_900_5
class_900_6
class_900_8
class_900_9
class_900_10)

for i in ${list[@]}
do
	echo $i
	cp $i/$i.csv ~/Google\ Drive/MIR/class_900/$i/
done
