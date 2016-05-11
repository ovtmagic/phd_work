#!/bin/bash

#-------------------------------------------------------------------------------
# Crea un directorio "to_remove"
# Mueve a este directorio todos los ficheros MIDI que solo tienen
# una o dos pistas.
#-------------------------------------------------------------------------------



mkdir to_remove

for i in `ls *mid *MID`
do 
	echo $i
	#line=`metamidi -l $i | cut -d ";" -f 5,13,34`
	#num_tracks=`echo $line|cut -d ";" -f 1`
	line=`metamidi -l $i | awk -F ";" '{ print $5 ";" $13 ";" $34 ;'}|tail -n 1`
	num_tracks=`echo $line|awk -F ";" '{ print $1; }'`
	#echo $num_tracks
	if [[ "$num_tracks" == "0" || "$num_tracks" == "1" || "$num_tracks" == "2" ]] 
	then 
		echo moving $i
		mv $i to_remove
	fi
	 
done


