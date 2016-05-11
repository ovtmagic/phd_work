#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint



#------------------------------------------------------------------------------
csv_column = 0 
if(len(sys.argv) == 3):
    #print sys.argv[1], sys.argv[2]
    file_csv = sys.argv[1]
    if sys.argv[2] == "bass":
        csv_column = 3
    elif sys.argv[2] == "melody":
        csv_column = 2 
    else:
        print "Error en argumentos:\n./run.py <csv_file> <bass|melody>"
        sys.exit(1)    
else:
    print "Error en argumentos:\n./run.py <csv_file> <bass|melody>"
    sys.exit(1)
    

# init histogram --------------------------------------------------------------
resolution = 1  # number of decimals
histogram = {}
for i in range(0, 10 ** resolution + 1):
    str_ = "%." + str(resolution) + "f"
    key = str_ % (i * 1.0 / 10 ** resolution)
    histogram[key] = 0 
#pprint(histogram)


str_format = "%." + str(resolution) + "f"  # "%.sf"
# Reading csv file ------------------------------------------------------------
f = open(file_csv)
for line in f.read().split("\n")[1:]:
    if line:
        line = line.replace('"', '')
        #print line
        num_tracks = line.split(",")[1]
        selected_tracks = line.split(",")[csv_column]
        
        for track in selected_tracks.split():
            key = str_format % (float(track) / float(num_tracks))
            histogram[key] = histogram[key] + 1
            #print ">>>", num_tracks, track, key
        

# print result as csv file
keys_ = histogram.keys()
keys_.sort()
for i in keys_:
    print "%s;%s" % (i.replace('.',','),str(histogram[i]))
    


