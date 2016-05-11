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
class_900_10)

> tmp.csv
rm -rf class
mkdir class

for i in ${list[@]}
do
	echo ">>>> $i"
	cat $i/$i.csv >> tmp.csv
	cp $i/$i/* class
done

chmod -R +r class

echo "\"Nombre_fichero\",N_Pistas,melody,bass,piano_rh,piano_lh,mixdown" > class.csv
sort -n tmp.csv |uniq|grep -v Nombre_fichero >> class.csv
#rm tmp.csv



