#!/usr/bin/python

import sys
import os
import random
import shutil
from pprint import pprint

list_genres=['class','jazz','kar']
#list_genres=['class']
src_lines={
    'class':[],
    'jazz':[],
    'kar':[]
}
sample_lines={
    'class':[],
    'jazz':[],
    'kar':[]
}



def create_dir(dst_path):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    dir_extr = ['class','class/class','jazz','jazz/jazz','kar','kar/kar']
    for d in dir_extr:
        if not os.path.exists(dst_path+"/"+d):
            os.mkdir(dst_path+"/"+d)
    

def write_csv(dst_path, name, v):
    #print dst_path+"/"+name+".csv"
    f = open(dst_path+"/"+name+".csv", 'w')
    f.write('"Nombre_fichero",N_Pistas,melody,bass,piano_rh,piano_lh,mixdown,accomp\n')
    for l in sorted(v, key=str.lower):
        f.write(l)
    f.close()
    



if len(sys.argv)!=4:
    print "Error en argumentos"
    print " ./crea_sample.sh <num_samples> <src_path> <dst_path>"
    sys.exit()

num_samples = int(sys.argv[1])
src_path = sys.argv[2]
dst_path = sys.argv[3]

# Read datasets
for g in list_genres:
    f = open(src_path+"/"+g+"/"+g+".csv", 'r')
    src_lines[g] = f.readlines()[1:]
    f.close()

# create sample full dataset
for g in list_genres:
    src = src_lines[g][:]
    for i in range(0, num_samples):
        r = int(random.random()*len(src))
        sample_lines[g].append(src[r])
        #print len(src),r
        del src[r]
          
     


# create csv
create_dir(dst_path)
for g in list_genres:
    l = len(sample_lines[g])
    write_csv(dst_path+"/"+g, g, sample_lines[g])
    write_csv(dst_path+"/"+g, g+"_train", sample_lines[g][l/3:])
    write_csv(dst_path+"/"+g, g+"_test", sample_lines[g][0:l/3])
    
# copy files
for g in list_genres:
    for l in sample_lines[g]:
        filename = l.split(',')[0]
        #print ">>>>>", src_path+"/"+g+"/"+g+"/"+filename, dst_path+"/"+g+"/"+g+"/"+filename
        src_file = src_path+"/"+g+"/"+g+"/"+filename
        dst_file = dst_path+"/"+g+"/"+g+"/"+filename
        shutil.copy(src_file, dst_file)
        