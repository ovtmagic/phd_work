#!/usr/bin/python

import os
import sys
import random
from pprint import pprint
import shutil

####################################################################################################
#
# hace un split de un directorio, pero 'barajando' los ficheros para que no sean consecutivos
# dentro de cada carpeta
####################################################################################################


ramdomize = True


# Se 'barajan' los ficheros. se debe evitar que en cada carpeta los ficheros sean consecutivos
def randomize_files(list_files):
	list_temp = []
	while list_files:
		i = int( random.random()*len(list_files) )
		item = list_files[i]
		list_temp.append(item)
		list_files.remove(item)
	return list_temp


# Divide el listado de ficheros en <num_folder> directorios con <files_by_folder> ficheros
def get_split_list(list_files, num_folders, files_by_folder):
	s = {}
	i = 0 
	j = 0
	list_temp = list_files[:]
	while i < num_folders and list_temp:
		j = 0
		s[i]=[]
		while j < files_by_folder and list_temp:
			#print ">>>>",i,j
			s[i].append(list_temp.pop())
			j = j+1 
		i = i+1
	if list_temp:
		s[i] = []
	while list_temp:
		s[i].append(list_temp.pop())
	return s
	
# genera los directorios y copia los ficheros
def do_split(s, folder):
	for i in s.keys():
		new_folder = "%s_%s" % (folder, i) 
		os.mkdir(new_folder)
		for file in s[i]:
			old_file = folder+"/"+file
			new_file = new_folder+"/"+file
			shutil.copy(old_file, new_file)



# comprobamos los argumentos
if len(sys.argv)<4:
	print "Error:\n\tsplit_folder.py <path> <num_folders> <files_by_folder>"
	exit(0)
folder = sys.argv[1]	
num_folders = int(sys.argv[2])
files_by_folder = int(sys.argv[3])
#print ">>>>", folder, num_folders, files_by_folder

# obtiene el listado de ficheros en el directorio
list_files = os.listdir(folder)
if ramdomize:
	list_files = randomize_files(list_files)

#se hace el split de las carpetas
s = get_split_list(list_files, num_folders, files_by_folder)
print s.keys()
do_split(s, folder)



