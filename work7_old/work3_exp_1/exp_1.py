#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint
import timing

# Variables ------------------------------------------------------------------------ 
#__train_file_extension__ = ".arff"  # .model or .arff
__train_file_extension__ = ".model"  # .model or .arff
path = "sample"
path_to_testfiles = "./tmp/"

# Experiment 1
exp1 = {
      'class':{'class', 'jazz', 'kar'},
      'jazz':{'class', 'jazz', 'kar'},
      'kar':{'class', 'jazz', 'kar'}
      }
pe_list = [0.01, 0.25, 0.5]


# cabecera tabla excel
cabecera=""
for i in pe_list:
    cabecera = "%s;%s" % (cabecera,i)
print cabecera
# esto lo utiliamos para revisar el resultado
result = ""
# corpus de test: jazz, class y kar
for corpus in exp1.keys():
    # for all midi files in a corpus the Tsmf2txt object is obtained ----------------------------------
    #print "# Loading %s" % (corpus)
    #print cabecera
    corpus_midifiles = {}
    #for midi_file in os.listdir(path_to_testfiles + corpus):
    csv = lmidi.TCsv(path + "/" + corpus + "/" + corpus + ".csv")
    for midi_file in csv.dic.keys():
        corpus_midifiles[midi_file] = lmidi.Tsmf2txt(path + "/" + corpus + "/" + corpus + "/" + midi_file, True)
    
    # arff files:   t=cl200, jz200, ....----------------------------------------------------------------
    for t in exp1[corpus]:
        arff_file = path +"/arff/" + t + __train_file_extension__
        line = "%s;%s" % (corpus, t)
        # Threshold error
        for pe in pe_list:
            #print corpus,t,pe
            success = 0.0
            error = 0.0
            # bass track selection successful 
            for m in corpus_midifiles.keys():
                try:
                    r = corpus_midifiles[m].get_selected_error('bass', arff_file, pe, csv)
                    if(r != 0):
                        error = error + 1
                    else:
                        success = success + 1
                except Exception as e:
                    print "Error: %s, %s" % (m, e)
            result = result + "%s;%s;%s;%s;%s;%s\n" % (corpus, t, pe, success / (success + error), success, error)
            line = "%s;%.3f" % (line, success / (success + error))
        print line.replace('.', ',')
          

print "\n\n", result
