#!/bin/bash


for i in `find ../../datasets/kar/kar -type f`
do 	
	echo $i
	smf2txt $i >> /dev/null
	ls -l
done
