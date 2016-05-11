#!/usr/bin/python
import os
import sys
import random
import lmidi
from pprint import pprint




def num_valid_tracks(path, filename):
    count = 0
    m = lmidi.Midi(path+"/"+filename, True)
    m.gen_descriptors()
    for t in m.tracks.keys():
        if m.tracks[t].is_valid():
            count = count + 1
    
    return count

# comprobamos los argumentos
if len(sys.argv)<3:
    print "Error:\n\check_tags.py <csv_file>"
    exit(0)
csv_filename = sys.argv[1]
path = sys.argv[2]

csv = lmidi.TCsv(csv_filename)

total = 0
count = 0
total_m = total_b = total_a = 0
for filename in sorted(csv.dic.keys(), key=str.lower):
    count = num_valid_tracks(path,filename)
    #print "\n\n#-----------------------------------\nFile: ",filename,"\n", count, csv.get_num_tracks(filename)
    m = set(csv.get(filename, 'melody'))
    b = set(csv.get(filename, 'bass'))
    a = set(csv.get(filename, 'accomp'))
    if m.intersection(b) or m.intersection(a) or b.intersection(a):
        print "\n\n#-----------------------------------\nFile: ",filename
        print m,b,a
    elif len(m)+len(b)+len(a) < count:
        print "\n\n#-----------------------------------\nFile: ",filename
        print "****",m,b,a,count,csv.get_num_tracks(filename)
    total = total + count
    total_m = total_m + len(m)
    total_b = total_b + len(b)
    total_a = total_a + len(a)
print "Total: ", total
print "  total m, b, a: ", total_m, total_b, total_a

