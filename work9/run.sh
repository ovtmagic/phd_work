#!/usr/bin/bash


echo class
get_prob_and_tags2.py ../datasets/arff/m_class.model ../datasets/arff/b_class.model  ../datasets/arff/a_class.model ../datasets/class/class.csv ../datasets/class/class/ > ../datasets/class/prob.txt
echo jazz
get_prob_and_tags2.py ../datasets/arff/m_jazz.model ../datasets/arff/b_jazz.model  ../datasets/arff/a_jazz.model ../datasets/jazz/jazz.csv ../datasets/jazz/jazz/ > ../datasets/jazz/prob.txt
echo kar
get_prob_and_tags2.py ../datasets/arff/m_kar.model ../datasets/arff/b_kar.model  ../datasets/arff/a_kar.model ../datasets/kar/kar.csv ../datasets/kar/kar/ > ../datasets/kar/prob.txt
