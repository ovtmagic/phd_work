#!/usr/bin/python
#===============================================================================
# Mejorando la eficiencia/velocidad del programa
#===============================================================================
import sys
import os
import re
import lmidi
from pprint import pprint
import timing
import gc


#===============================================================================

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


# Variables ------------------------------------------------------------------------


__max_files__ = 3000  # numero de ficheros midi que se van a utilizar en el test
__train_extension__ = ".model"

path_to_arff = "/home/octavio/Dropbox/MIR/Datasets/arff/"
path_to_testfiles = "/tmp/mir/"

# Experiment 2
exp2 = {
      'clasica':['cl200', 'jzkr200', 'cljzkr200'],
      'jazz':['jz200', 'clkr200', 'cljzkr200'],
      'kar':['kr200', 'cljz200', 'cljzkr200']
      }
exp2 = {
      'kar':['kr200', 'cljz200', 'cljzkr200'],
      }
pe_list = [0.01]



counter=1

corpus_test_2=[]
# corpus de test: jaz, clasica y kar
for corpus in exp2.keys():
    # for all midi files in a corpus the Tsmf2txt object is obtained ----------------------------------
    lmidi.testTime.start('A1')
    #print "# Loading %s" % (corpus)
    corpus_midifiles = {}
    for midi_file in os.listdir(path_to_testfiles + corpus):
        # se comprueba si el fichero acaba en .txt
        if not re.search(".sky",midi_file) and counter <=__max_files__:
            #print "(%s)\t%s" % (counter,midi_file)
            counter+=1
            m=lmidi.Tsmf2txt(path_to_testfiles + corpus + "/" + midi_file, True, format='midi')
            m.gen_descriptors()
            m.remove_notes()
            corpus_midifiles[midi_file] = m
            
            
    lmidi.testTime.stop('A1')
    lmidi.testTime.start('A2')
    csv = lmidi.TCsv(path_to_arff + corpus + ".csv")
    lmidi.testTime.stop('A2')
    # fichero arff de test -------------------------------------------------
    lmidi.testTime.start('A3')
    arff_test_filename, instance = create_arff_test(corpus, corpus_midifiles)
    lmidi.testTime.stop('A3')
    #pprint(instance)
    
    
    # arff files:   t=cl200, jz200, ....----------------------------------------------------------------
    for t in exp2[corpus]:
        arff_file = path_to_arff + t + __train_extension__
        lmidi.testTime.start('B1')
        prob_midifile = get_prob_midifiles(arff_test_filename, instance, arff_file)
        lmidi.testTime.stop('B1')
        #pprint(prob_midifile)      
        
        # FIN se obtinen las probabilidades  --------------------------------------
        # Threshold error
        for pe in pe_list:
            #print corpus,t,pe
            success = 0.0
            error = 0.0
            # bass track selection successful 
            for m in corpus_midifiles.keys():
                try:
                    lmidi.testTime.start('B2')
                    #r = corpus_midifiles[m].get_selected_error('bass', arff_file, pe, csv)
                    r = corpus_midifiles[m].get_selected_error('bass', arff_file, pe, csv,prob_midifile[m])
                    lmidi.testTime.stop('B2')
                    #r=0
                    if(r != 0):
                        error = error + 1
                    else:
                        success = success + 1
                except Exception as e:
                    print "Error: %s, %s" % (m,e)
                
            print "%s;%s;%s;%s;%s;%s" % (corpus, t, pe, 100 * success / (success + error), success, error)
        

lmidi.testTime.imp()
