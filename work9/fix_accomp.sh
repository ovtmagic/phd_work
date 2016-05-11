#!/usr/bin/bash




for i in `find ../datasets/class -type f -name "*.csv"`
do
	echo $i
	wc -l $i
	./fix_accomp.py $i ../datasets/class/class > xtmp
	cp xtmp $i
	wc -l $i
done


for i in `find ../datasets/jazz -type f -name "*.csv"`
do
	echo $i
	wc -l $i
	./fix_accomp.py $i ../datasets/jazz/jazz > xtmp
	cp xtmp $i
	wc -l $i
done


for i in `find ../datasets/kar -type f -name "*.csv"`
do
	echo $i
	wc -l $i
	./fix_accomp.py $i ../datasets/kar/kar > xtmp
	cp xtmp $i
	wc -l $i
done
