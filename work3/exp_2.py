#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint


# Variables ------------------------------------------------------------------------ 
__train_file_extension__ = ".model"  # .model or .arff
path_to_arff = "/home/octavio/Dropbox/MIR/Datasets/arff/"
path_to_testfiles = "/tmp/mir/"

# Experiment 2
exp2 = {
      'clasica':['cl200', 'jzkr200', 'cljzkr200'],
      'jazz':['jz200', 'clkr200', 'cljzkr200'],
      'kar':['kr200', 'cljz200', 'cljzkr200']
      }
pe_list = [0.01]


# cabecera tabla excel
print ";igual;diferentes;todos"
# esto lo utiliamos para revisar el resultado
result=""

# corpus de test: jaz, clasica y kar
for corpus in exp2.keys():
    # for all midi files in a corpus the Tsmf2txt object is obtained ----------------------------------
    #print "# Loading %s" % (corpus)
    corpus_midifiles = {}
    for midi_file in os.listdir(path_to_testfiles + corpus):
        corpus_midifiles[midi_file] = lmidi.Tsmf2txt(path_to_testfiles + corpus + "/" + midi_file, True)
    csv = lmidi.TCsv(path_to_arff + corpus + ".csv")
    line = corpus
    # arff files:   t=cl200, jz200, ....----------------------------------------------------------------
    for t in exp2[corpus]:
        arff_file = path_to_arff + t + __train_file_extension__
        # Threshold error
        for pe in pe_list:
            #print corpus,t,pe
            success = 0.0
            error = 0.0
            # bass track selection successful 
            for m in corpus_midifiles.keys():
                try:
                    r = corpus_midifiles[m].get_selected_error('bass', arff_file, pe, csv)
                    #r=0
                    if(r != 0):
                        error = error + 1
                    else:
                        success = success + 1
                except Exception as e:
                    print "Error: %s, %s" % (m, e)
            #print "%s;%s;%s;%s;%s;%s" % (corpus, t, pe, 100 * success / (success + error), success, error)
            result = result + "%s;%s;%s;%s;%s;%s\n" % (corpus, t, pe, success / (success + error), success, error)
            line = "%s;%.3f" % (line, success / (success + error))
    print line.replace('.', ',')


print "\n\n",result
