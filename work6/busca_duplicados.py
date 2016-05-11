#!/usr/bin/python
#===============================================================================
# Busca ficheros midi duplicados:
# ./busca_duplicados.py <paht1> <path2> .... <pathn>
# la busqueda la realiza comparando el tamano de los ficheros, o comparando el
# hash md5 de los ficheros
#===============================================================================

import os
import sys
import hashlib


# devuelve el tamano de un fichero
def get_size(file_name):
    return os.stat(file_name).st_size

# devuelve el hash md5 de un fichero
def get_md5(file_name):
    f = open(file_name)
    hash_md5 = hashlib.md5(f.read()).hexdigest()
    f.close()
    return hash_md5


# file_dic[file_size]=file_name
file_dic = {}


# se obtiene la informacion de todos los ficheros y se guarda en file_dic
for path in sys.argv[1:]:
    for f in os.listdir(path):
        file_name = path + "/" + f
        file_size = get_md5(file_name) 
        if not file_size in file_dic.keys():
            file_dic[file_size] = []
        file_dic[file_size].append(file_name)

# se buscan duplicados
for s in file_dic.keys():
    if len(file_dic[s]) > 1:
        for f in file_dic[s]:
            print s, f
        print "%---------------------"
