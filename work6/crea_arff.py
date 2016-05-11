#!/usr/bin/python
#===============================================================================
# ./arff.py <bass|melody> <file.arff> <"corpus1.csv corpus2.csv ..."> <"corpus_dir1  corpus_dir2 .... ">
#
# ./arff.py <bass|melody> <file.arff> <corpus1.csv> <corpus_dir1>
# 
# file.arff: es el fichero arff para weka que se crea
# corpusx.csv: es el fichero csv que corresponde al directorio corpus_dirx
# corpus_dirx: es el nombre del directorio que contiene los ficheros MIDI. Por
# cada directorio debe existir un fichero corpus_dirx.csv con las etiquetas de
# las pistas que corresponden al bajo o la melodia
#===============================================================================
import sys
import os
import lmidi
from pprint import pprint


if(len(sys.argv) < 3):
    print "Error:"
    print "./arff.py <bass|melody> <file.arff> <\"file1.csv file2.csv ...\"> <\"corpus_dir1 corpus_dir2 ...>\n"
    sys.exit(1)
else:
    print "* CSV files: ", sys.argv[3]
    print "* MIDI files paths: ", sys.argv[4]
    csv_argv = sys.argv[3].split()
    dir_argv = sys.argv[4].split()
    if len(csv_argv) != len (dir_argv):
        print "Error:"
        print "\tYou must use the same number of csv files than corpus_dir"
        sys.exit(1)

tracktype = sys.argv[1]
file_arff = sys.argv[2]
# diccionario (dir midi files, csv file)
dic_corpus = {}
for i in range(len(csv_argv)):
    dic_corpus[dir_argv[i]] = csv_argv[i]



arff = ""
# check all corpus/directories containing MIDI files
midifiles = {}
for corpus in dic_corpus.keys():
    csvfile = dic_corpus[corpus]
    print "  * ",tracktype,file_arff,corpus, csvfile
    #csvfile = "%s.csv" % corpus
    csv = lmidi.TCsv(csvfile)
    
    # Check all files into a corpus/directory
    for filename in os.listdir(corpus):
        class_ok = csv.get(filename, tracktype)
        # si el fichero midi no esta en el fichero csv no se hace nada
        if class_ok != -1:
            #print ">>",tracktype,file_arff,corpus,filename,class_ok
            
            m = lmidi.Midi()
            m.load_midi(corpus + "/" + filename)
            m.load_skyline(corpus + "/" + filename)
            m.gen_descriptors()
            
            if not arff:
                arff = m.get_arff_header(tracktype + "_" + corpus)
            #print ">",filename
            arff = arff + m.get_arff(class_ok)
        
# write the arff file
f = open(file_arff, "w")
f.write(arff)
f.close()
