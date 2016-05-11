#!/bin/bash

filename="class_900.con_notas.csv"
train_file=$1
path="class_900"

for i in `egrep -v ";M|;OK|Quitar|Nombre_fichero" ${filename}|awk -F "," '{ print $1; }'`
do
	echo $i
	../get_probabilities.py ${train_file} ${path}/$i
	read x
	clear
done
