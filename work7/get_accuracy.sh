#!/usr/bin/bash


#-------------------------------------------------------
# Obtiene la tasa de acierto, falsos positivos, etc, ....
# en la clasificacion. Lo hace para los datasets de bajo y
# melodia, para cada uno de los "paquetes" creados de class_900
#-------------------------------------------------------



weka_jar="weka.jar weka.classifiers.trees.RandomForest -K 6 -I 10"
m_train="arff/m_clasica.arff"
b_train="arff/b_clasica.arff"

m_list=(m_class_900_0.arff
m_class_900_1.arff
m_class_900_2.arff
m_class_900_3.arff
m_class_900_4.arff
m_class_900_5.arff
m_class_900_6.arff
m_class_900_8.arff
m_class_900_9.arff
m_class_900_10.arff
)

b_list=(b_class_900_0.arff
b_class_900_1.arff
b_class_900_2.arff
b_class_900_3.arff
b_class_900_4.arff
b_class_900_5.arff
b_class_900_6.arff
b_class_900_8.arff
b_class_900_9.arff
b_class_900_10.arff
)



echo "File,TT,FN,FP,TN"

for i in ${m_list[@]}
do
	java -cp $weka_jar -t $m_train  -T arff/$i > .tmpresult
	acc=`grep "Correctly Classified Instances" .tmpresult|tail -1 |awk  '{print $5;}'`
	TT=`grep "=" .tmpresult|tail -2 |grep yes|awk '{ print $1;}'`
	FN=`grep "=" .tmpresult|tail -2 |grep yes|awk '{ print $2;}'`
	FP=`grep "=" .tmpresult|tail -2 |grep no|awk '{ print $1;}'`
	TN=`grep "=" .tmpresult|tail -2 |grep no|awk '{ print $2;}'`
	echo $i,$acc,$TT,$FN,$FP,$TN
done

echo
echo

for i in ${b_list[@]}
do
	java -cp $weka_jar -t $b_train  -T arff/$i > .tmpresult
	acc=`grep "Correctly Classified Instances" .tmpresult|tail -1 |awk  '{print $5;}'`
	TT=`grep "=" .tmpresult|tail -2 |grep yes|awk '{ print $1;}'`
	FN=`grep "=" .tmpresult|tail -2 |grep yes|awk '{ print $2;}'`
	FP=`grep "=" .tmpresult|tail -2 |grep no|awk '{ print $1;}'`
	TN=`grep "=" .tmpresult|tail -2 |grep no|awk '{ print $2;}'`
	echo $i,$acc,$TT,$FN,$FP,$TN
done
