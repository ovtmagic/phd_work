#!/bin/bash



#weka_jar="java -cp weka.jar weka.classifiers.trees.RandomForest -K 6 -I 10 "
weka_jar="java -cp /Applications/weka-3-6-11-oracle-jvm.app/Contents/Java/weka.jar weka.classifiers.trees.RandomForest -K 6 -I 10 "

if [ "$2" == "" ]
then
	echo "Error, falta un parametro"
    exit 1
else
	echo params: $1 $2
	$weka_jar -t $1  -d $2
fi
