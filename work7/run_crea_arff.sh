
#!/usr/bin/bash

arff_cmd="arff.py"

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

for i in ${list[@]}
do
	echo $i
	$arff_cmd melody csv/$i.csv class > arff/m_${i}.arff
	$arff_cmd bass csv/$i.csv class > arff/b_${i}.arff
done
