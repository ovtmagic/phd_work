#!/usr/bin/bash


mv class/class.csv backup
../work9/extend_csv.py backup/class.csv > class/class.csv

mv class/class_test.csv backup
../work9/extend_csv.py backup/class_test.csv > class/class_test.csv

mv class/class_train.csv backup
../work9/extend_csv.py backup/class_train.csv > class/class_train.csv



mv jazz/jazz.csv backup
../work9/extend_csv.py backup/jazz.csv > jazz/jazz.csv

mv jazz/jazz_test.csv backup
../work9/extend_csv.py backup/jazz_test.csv > jazz/jazz_test.csv

mv jazz/jazz_train.csv backup
../work9/extend_csv.py backup/jazz_train.csv > jazz/jazz_train.csv



mv kar/kar.csv backup
../work9/extend_csv.py backup/kar.csv > kar/kar.csv

mv kar/kar_test.csv backup
../work9/extend_csv.py backup/kar_test.csv > kar/kar_test.csv

mv kar/kar_train.csv backup
../work9/extend_csv.py backup/kar_train.csv > kar/kar_train.csv

