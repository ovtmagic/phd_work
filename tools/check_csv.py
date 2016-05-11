#!/usr/bin/python
import os
import sys
import random
from pprint import pprint


# comprobamos los argumentos
if len(sys.argv)<3:
	print "Error:\n\check_csv.py <csv_file> <folder>"
	exit(0)
csv_filename = sys.argv[1]
foldername = sys.argv[2]	

temp = open(csv_filename, 'r').read().splitlines()
csv_files = [i.split(',')[0].replace('"','') for i in temp]
folder_files = os.listdir(foldername)


for i in csv_files[:]:
	if i in folder_files:
			csv_files.remove(i)
			folder_files.remove(i)

print "Not in Folder:", len(csv_files)
pprint(csv_files)
print "-----------"
print "Not in CSV file:", len(folder_files)
pprint(folder_files)