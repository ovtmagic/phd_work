#!/usr/bin/python
import sys
import os
import re
import lmidi
from pprint import pprint





#--------------------------------------------------

if(len(sys.argv) == 3):
    #print sys.argv[1], sys.argv[2]
    csv_file = sys.argv[1]
    corpus = sys.argv[2]
else:
    print "Error en argumentos:\n./csv_melody_tagger.py <csv_file> <corpus>"
    sys.exit(1)
#print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'
midi_path = "/tmp/mir/%s/" % (corpus)
debug = False


f = open(csv_file, 'r')
file_lines = f.readlines()
f.close()


csv_result = file_lines[0]

# read all file lines
for line in file_lines[1:]:
    # gets fields for each line -----------------------------------------------
    fields = line.split(',')
    file_name = fields[0]
    m = lmidi.Tsmf2txt(midi_path + file_name)
    # for each file gets track name (lower case) and track number -------------
    melody_tracks=""
    for t in m.tracks.keys():
        track_name=m.tracks[t].name.lower()
        track_number=m.tracks[t].number
        # checks if track name contains bbok or melody
        if re.search('bbok',track_name) or re.search('melody', track_name):
            melody_tracks = melody_tracks + str(track_number) + " "
        if debug:
            print "    %s,\t%s,\t%s" % (file_name, track_number, track_name)
    # new csv line with melody tracks is created ------------------------------
    new_line = fields[0]
    for i in range(1, len(fields)):
        # if field number == 2 melody tracks is writen
        if i == 2:
            new_line = new_line + "," + melody_tracks
        else:
            new_line = new_line + "," + fields[i]  
    # global result (csv_result) is upgraded
    csv_result = csv_result + new_line
    if debug:
        print new_line[:-1]
    
    
if not debug:
    print csv_result

