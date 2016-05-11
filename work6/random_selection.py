#!/usr/bin/python
#===============================================================================
# Hace una seleccon aleatorio de <num> ficheros de un directorio <src> y los
# copia en el directorio <dst>. En el caso de que hayan varios directorios 
# anidados, renombra el fichero y pone en el nombre el path del fichero 
# original. Por ejemplo:
#  el fichero <src>/dir1/dir2/dir3/file1.mid lo copia como:
#  <dst>dir1_dir2_dir3_file1.mid
#
# Uso:
#  ./random_selection.py <num> <src> <dst> [filter]
# filter puede ser, por ejemplo, *mid (de momento, esto no esta implementado)
#===============================================================================
import sys
import os
import random
import shutil




if(len(sys.argv) < 3):
    print "Error:"
    print "./random_selection.py <num> <src> <dst>\n"
    sys.exit(1)
else:
    num_files = sys.argv[1]
    src = sys.argv[2]
    dst = sys.argv[3]
    
    
# Gets files from src
file_list = []

f = os.popen("find %s -type f" % src)
for i in f.read().split('\n'):
    file_list.append(i)
f.close()


os.makedirs(dst)
# Random selection
dst_file_list = []
for i in range(0, int(num_files)):
    index = int(random.random() * len(file_list))
    file_name = file_list[index]
    file_list.pop(index)
    new_file_name = dst + "/" + file_name.split('/')[0]
    for j in file_name.split('/')[1:]:
        new_file_name = new_file_name + "_" + j
    #new_file_name = dst + "/" + file_name.split('/')[-1]
    print " copying: %s\t\t%s" % (file_name, new_file_name)
    shutil.copy(file_name, new_file_name)
