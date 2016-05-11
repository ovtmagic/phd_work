#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint
import timing


# ------------------------------------------------------------------------------
def get_prob_midifiles(arff_test_filename, instance, arff_file):
    # se obtinen las probabilidades  --------------------------------------
    prob_instance = lmidi.get_probabilites(arff_file, arff_test_filename, False)
    #print "#>>>>>>>", len(prob_instance)
    #print "#>>>>>>>", prob_instance
    #print "#>>>>>>>"
    prob_midifile = {}
    # se obtiene la probabilidad de cada instancia (linea de prob. de weka) y se agrupa por
    # el fichero MIDI. Para cada fichero MIDI se tiene un vector con la probabilidad de cada
    # pista valida
    for i in prob_instance.keys():
        midi_file = instance[i]['midi_file']
        prob = prob_instance[i]
        if not midi_file in prob_midifile.keys():
            prob_midifile[midi_file] = []
        prob_midifile[midi_file].append(prob)
    # las probabilidades de las piestas estan como arrays, se pasan a diccionarios para
    # poder utilizarlas en las funciones de lmidi
    prob_midifile_dic={}
    for m in prob_midifile.keys():
        prob_midifile_dic[m]={}
        for i in range( len(prob_midifile[m]) ):
            prob_midifile_dic[m][i+1] = prob_midifile[m][i]
    return prob_midifile_dic

def create_arff_test(corpus, corpus_midifiles):
    counter_instances = 1
    instance = {}
    arff_test = ""
    arff_test_filename = "/tmp/%s.arff" % (corpus)
    print "#>>>>", arff_test_filename
    for m in corpus_midifiles.keys():
        if not arff_test:
            arff_test = corpus_midifiles[m].get_arff_header(corpus)
        for l in corpus_midifiles[m].get_arff([]).split("\n"):
            if (l):
                instance[counter_instances] = {'arff_line':l,
                    'midi_file':m,
                    'prob':0}
                arff_test = arff_test + l + "\n"
                counter_instances += 1
    
    f = open(arff_test_filename, "w")
    f.write(arff_test)
    f.close()
    return arff_test_filename, instance


# Variables -------------------------------------------------------------------- 
__train_file_extension__ = ".arff"  # .model or .arff
#path_to_arff = "/home/octavio/Dropbox/MIR/Datasets/arff/"
path_to_arff = "/Users/octavio/Dropbox/MIR/Datasets/arff/"
path_to_testfiles = "/tmp/mir/"

# Experiment 1
exp1 = {
      'clasica':['cl200', 'jz200', 'kr200'],
      'jazz':['cl200', 'jz200', 'kr200'],
      'kar':['cl200', 'jz200', 'kr200']
      }
exp1 = {
      'kar':['cl200', 'jz200', 'kr200']
      }
pe_list = [0.01, 0.25, 0.5]
# ------------------------------------------------------------------------------

# cabecera tabla excel
cabecera=""
for i in pe_list:
    cabecera = "%s;%s" % (cabecera,i)
print cabecera
# esto lo utiliamos para revisar el resultado
result = ""
# corpus de test: jaz, clasica y kar
for corpus in exp1.keys():
    # for all midi files in a corpus the Tsmf2txt object is obtained ----------------------------------
    #print "# Loading %s" % (corpus)
    #print cabecera
    corpus_midifiles = {}
    for midi_file in os.listdir(path_to_testfiles + corpus):
        corpus_midifiles[midi_file] = lmidi.Tsmf2txt(path_to_testfiles + corpus + "/" + midi_file, True)
    csv = lmidi.TCsv(path_to_arff + corpus + ".csv")
    # creacion del fichero arff de test
    arff_test_filename, instance = create_arff_test(corpus, corpus_midifiles)
    
    # arff training files:   t=cl200, jz200, ....------------------------------------------------------
    for t in exp1[corpus]:
        arff_file = path_to_arff + t + __train_file_extension__
        line = "%s;%s" % (corpus, t)
        # obtencion de la probabilidad de bajo de cada pista MIDI
        prob_midifile = get_prob_midifiles(arff_test_filename, instance, arff_file)
        # Threshold error
        for pe in pe_list:
            #print corpus,t,pe
            success = 0.0
            error = 0.0
            # bass track selection successful 
            for m in corpus_midifiles.keys():
                try:
                    #r = corpus_midifiles[m].get_selected_error('bass', arff_file, pe, csv)
                    r = corpus_midifiles[m].get_selected_error('bass', arff_file, pe, csv, prob_midifile[m])
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
