#!/bin/bash



#weka_jar="java -cp weka.jar weka.classifiers.trees.RandomForest -K 6 -I 10 "
weka_jar="java -cp weka.jar weka.classifiers.trees.RandomForest -K 6 -I 10 "

if [ "$2" == "" ]
then
	echo params: $1 
	$weka_jar -t $1
else
	echo params: $1 $2
	$weka_jar -t $1  -T $2
fi
