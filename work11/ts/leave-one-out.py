#!/usr/bin/python
#===============================================================================
# Seleccion bajo/melodia utilizando leave-one-out
#
# ./leave-one-out.py <bass|melody> <threshold > <csv_file> <path_to_files>
#    <bass|melody>
#    <csv_file>: fichero con las etiquetas
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
import lmidi
#import cyg_lmidi as lmidi
from pprint import pprint
#import timing


#testTime = timing.Timing()


#--------------------------------------------------------------------------------
# crea el fichero arff
def write_file(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()

# crea los ficheros arff de train y test
def create_arff_file(one, all):
    test_file = arff_header + arff_list[one]
    train_file = arff_header
    for i in all:
        train_file = train_file + arff_list[i] + "\n"
    write_file("tmp/test.arff",test_file)
    write_file("tmp/train.arff",train_file)
    
def leave_one_out(lista):
    result = []
    for one in lista:
        all=[]
        for i in lista:
            if i != one:
                all.append(i)
        result.append((one, all))
    return result
 
#--------------------------------------------------------------------------------
if (len(sys.argv) == 2 and sys.argv[1] == "header"):
    print "Total:Filename,track type,Acc.%,Error 0,Error 1,Error 2,Error 3,TP,FP,FN,TN,Precision,Recall,F-measure"
    sys.exit(0)
    
if (len(sys.argv) == 5):
    track_type = sys.argv[1]
    threshold = float(sys.argv[2])
    csv_filename = sys.argv[3]
    path = sys.argv[4]
else:
    print """ ./get_prob_and_tags.py <bass|melody> <threshold> <csv_file> <path_to_files>
        <bass|melody>
        <csv_file>: fichero con las etiquetas
        <path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)
debug = False
#--------------------------------------------------------------------------------


# leemos el fichero csv
csv = lmidi.TCsv(csv_filename)
midi_list = {}
arff_list = {}
arff_header = ""
total_errors = {0:0, 1:0, 2:0, 3:0}
confusion_matrix = {'TP':0, 'FP':0, 'FN':0, 'TN':0}

# read all midi files and get the arff lines for each file
for filename in sorted(csv.dic.keys(), key=str.lower):
    m = lmidi.Midi(path+"/"+filename, True)
    midi_list[filename] = m
    midi_list[filename].gen_descriptors()
    class_ok = csv.get(filename, track_type)
    arff_list[filename] = midi_list[filename].get_arff(class_ok)
    #print arff_list[filename]
    if not arff_header:
        arff_header = midi_list[filename].get_arff_header() + "\n"
    
# Leave one out
loo_list = leave_one_out(csv.get_files())

count = 0
# Create arff files and get error type for each file
for i in loo_list:
    #for i in [ x for x in loo_list if x[0] in ['Renaissance_Renaissance-Late_Victoria_Quam_Pulchri_Sunt-2-Gloria-c.mid','Medieval_ArsNova_Machau_machaut-b17.mid','Renaissance_Renaissance-Late_Victoria_Quicumque_Christum_Quaeritis-s.mid']]:    
    midi_filename = i[0]
    print ">>>>", midi_filename
    create_arff_file(midi_filename,i[1])
    # fichero seleccionado
    m = midi_list[midi_filename]
    prob = lmidi.get_probabilites("tmp/train.arff", "tmp/test.arff", debug)
    track_selected = m.get_selected_track("tmp/train.arff", "tmp/test.arff", threshold, prob)
    error = m.get_selected_error(track_type, "tmp/train.arff", threshold, csv, prob)
    #"""
    print prob
    print lmidi.get_prob_iB(prob, threshold)
    print track_selected
    #"""
    (TP, FP, FN, TN) = m.get_confusion_matrix(track_type, "tmp/train.arff", threshold, csv, prob)
    #print error,prob
    total_errors[error] = total_errors[error] + 1
    confusion_matrix['TP'] = confusion_matrix['TP'] + TP
    confusion_matrix['FP'] = confusion_matrix['FP'] + FP
    confusion_matrix['FN'] = confusion_matrix['FN'] + FN
    confusion_matrix['TN'] = confusion_matrix['TN'] + TN
    count = count + 1
    if not count % 10:
        write_file("tmp/count.txt",str(count))
    print "File:%s,%s,%s,%s,%s,%s,%s" % (midi_filename, track_type, track_selected, TP, FP, FN, TN)
    

precision = lmidi.get_precision( confusion_matrix['TP'], confusion_matrix['FP'] )
recall = lmidi.get_recall( confusion_matrix['TP'], confusion_matrix['FN'] )
f_m = lmidi.get_f_measure( precision, recall)
accuracy = 100.0*total_errors[0]/(total_errors[0]+total_errors[1]+total_errors[2]+total_errors[3])

print "Total:%s,%s,%.2f%%,%s,%s,%s,%s,%s,%s,%s,%s,%.2f,%.2f,%.2f" % (csv_filename.split("/")[-1], track_type, accuracy, total_errors[0], total_errors[1], total_errors[2], total_errors[3], confusion_matrix['TP'], confusion_matrix['FP'], confusion_matrix['FN'],  confusion_matrix['TN'], precision, recall, f_m)
