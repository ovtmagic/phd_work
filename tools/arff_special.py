#!/usr/bin/python
#===============================================================================
# ./arff.py <bass|melody> <file.arff> <corpus_dir1  corpus_dir2 .... >
# 
# file.arff: es el fichero arff para weka que se crea
# corpus_dirx: es el nombre del directorio que contiene los ficheros MIDI. Por
# cada directorio debe existir un fichero corpus_dirx.csv con las etiquetas de
# las pistas que corresponden al bajo o la melodia
#===============================================================================
import sys
import os
import lmidi
#import cyg_lmidi as lmidi
from pprint import pprint


if( len(sys.argv) != 4):
    print "Error:"
    print "./arff.py <bass|melody> <csv_file> <path_to_files>\n"
    sys.exit(1)

tracktype = sys.argv[1]
csv_file = sys.argv[2]
path = sys.argv[3]


arff = ""
csv = lmidi.TCsv(csv_file)

# check all corpus/directories containing MIDI files
midifiles = {}
    
# Check all files into a corpus/directory
for filename in csv.get_files():
    if tracktype == "melody":
        class_ok = csv.get(filename, 'melody') + csv.get(filename, 'piano_rh')
        print csv.get(filename, 'melody') , csv.get(filename, 'piano_rh')
    if tracktype == "bass":
        class_ok = csv.get(filename, 'bass') + csv.get(filename, 'piano_lh')
        print csv.get(filename, 'bass') , csv.get(filename, 'piano_lh')
    print ">>",tracktype,filename,class_ok,"\n"
    
    m = lmidi.Midi(path+"/"+filename, True)
    m.gen_descriptors()
    
    if not arff:
        arff = m.get_arff_header(tracktype + "_" + csv_file)
    print ">>>>>",class_ok
    arff = arff + m.get_arff(class_ok)
    print m.get_arff(class_ok)
    print 
    print 
        
# print the arff file
#print arff
