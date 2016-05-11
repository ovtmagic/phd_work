#!/bin/bash

rm res1.csv

leave-one-out.py melody ../csv/clas200.csv ../old_datasets/clas200 >> res1.csv
leave-one-out.py melody ../csv/clasica.csv ../old_datasets/clasica >> res1.csv
leave-one-out.py melody ../csv/class_900.csv ../old_datasets/class_900 >> res1.csv

leave-one-out.py bass ../csv/clas200.csv ../old_datasets/clas200 >> res1.csv
leave-one-out.py bass ../csv/clasica.csv ../old_datasets/clasica >> res1.csv
leave-one-out.py bass ../csv/class_900.csv ../old_datasets/class_900 >> res1.csv
