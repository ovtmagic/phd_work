#!/bin/bash

arff="arff.py"

# melody
${arff} melody class/class.csv class/class > arff/m_class.arff
${arff} melody class/class_test.csv class/class > arff/m_class_test.arff
${arff} melody class/class_train.csv class/class > arff/m_class_train.arff

${arff} melody jazz/jazz.csv jazz/jazz > arff/m_jazz.arff
${arff} melody jazz/jazz_test.csv jazz/jazz > arff/m_jazz_test.arff
${arff} melody jazz/jazz_train.csv jazz/jazz > arff/m_jazz_train.arff

${arff} melody kar/kar.csv kar/kar > arff/m_kar.arff
${arff} melody kar/kar_test.csv kar/kar > arff/m_kar_test.arff
${arff} melody kar/kar_train.csv kar/kar > arff/m_kar_train.arff


# bass
${arff} bass class/class.csv class/class > arff/b_class.arff
${arff} bass class/class_test.csv class/class > arff/b_class_test.arff
${arff} bass class/class_train.csv class/class > arff/b_class_train.arff

${arff} bass jazz/jazz.csv jazz/jazz > arff/b_jazz.arff
${arff} bass jazz/jazz_test.csv jazz/jazz > arff/b_jazz_test.arff
${arff} bass jazz/jazz_train.csv jazz/jazz > arff/b_jazz_train.arff

${arff} bass kar/kar.csv kar/kar > arff/b_kar.arff
${arff} bass kar/kar_test.csv kar/kar > arff/b_kar_test.arff
${arff} bass kar/kar_train.csv kar/kar > arff/b_kar_train.arff


# accompaniment
${arff} accomp class/class.csv class/class > arff/a_class.arff
${arff} accomp class/class_test.csv class/class > arff/a_class_test.arff
${arff} accomp class/class_train.csv class/class > arff/a_class_train.arff

${arff} accomp jazz/jazz.csv jazz/jazz > arff/a_jazz.arff
${arff} accomp jazz/jazz_test.csv jazz/jazz > arff/a_jazz_test.arff
${arff} accomp jazz/jazz_train.csv jazz/jazz > arff/a_jazz_train.arff

${arff} accomp kar/kar.csv kar/kar > arff/a_kar.arff
${arff} accomp kar/kar_test.csv kar/kar > arff/a_kar_test.arff
${arff} accomp kar/kar_train.csv kar/kar > arff/a_kar_train.arff

