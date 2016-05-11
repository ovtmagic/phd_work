#!/bin/bash

get_prob_and_tags2_loo.py class/class.csv class/class > prob/prob_class.txt
get_prob_and_tags2_loo.py class/class_train.csv class/class > prob/prob_class_train.txt

get_prob_and_tags2_loo.py jazz/jazz.csv jazz/jazz > prob/prob_jazz.txt
get_prob_and_tags2_loo.py jazz/jazz_train.csv jazz/jazz > prob/prob_jazz_train.txt

get_prob_and_tags2_loo.py kar/kar.csv kar/kar > prob/prob_kar.txt
get_prob_and_tags2_loo.py kar/kar_train.csv kar/kar > prob/prob_kar_train.txt
