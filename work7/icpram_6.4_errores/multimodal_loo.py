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
# Seleccion multimodal
#--------------------------------------------------------------------------------



def get_track_multimodal(prob_bass, prob_melody, thres, m):
    # se pasan como argumentos las probabilidades p(B|i) y p(M|i)
    # hay que calcular p(i|B) y p(i|M)
    prob_iB = lmidi.get_prob_iB(prob_bass, thres)
    prob_iM = lmidi.get_prob_iB(prob_melody, thres)
    # a saco
    prob_iM[-1] = 0.0
    # se obtiene el vector "multimodal" iB
    iB = {}
    for i in prob_iB.keys():
        iB[i] = prob_iB[i]*(1.0-prob_iM[i])
    x = 0.0
    for i in prob_iB.keys():
        x = x + prob_iB[i]
    # Se busca la pista que maximiza iB
    max_prob_iB = 0.0
    max_i = -1
    for i in iB.keys():
        #print ">>>>>>>",i,iB[i],max_prob_iB
        if iB[i] >= max_prob_iB:
            max_prob_iB = iB[i]
            max_i = i
    # devuele el numero de pista real en el fichero midi
    """print prob_bass
    print prob_melody
    print prob_iB
    print prob_iM
    print iB
    print max_i"""
    return m.gno(max_i)
    
    
    






#--------------------------------------------------------------------------------
# crea el fichero arff
def write_file(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()

# crea los ficheros arff de train y test
def create_arff_file(one, all):
    # fichero arrf bass
    test_file = arff_header + arff_list_bass[one]
    train_file = arff_header
    for i in all:
        train_file = train_file + arff_list_bass[i] + "\n"
    write_file("tmp/b_test.arff",test_file)
    write_file("tmp/b_train.arff",train_file)
    # fichero arrf melody
    test_file = arff_header + arff_list_melody[one]
    train_file = arff_header
    for i in all:
        train_file = train_file + arff_list_melody[i] + "\n"
    write_file("tmp/m_test.arff",test_file)
    write_file("tmp/m_train.arff",train_file)
    
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
    print "Filename;track type;Acc.%,Error 0;Error 1;Error 2;Error 3;TP;FP;FN;TN;Precision;Recall;F-measure"
    sys.exit(0)
    
if (len(sys.argv) == 6):
    # se selecciona esta pista (bass)
    track_type_bass = sys.argv[1]
    # teniendo en cuenta la informacion de esta pista (melody)
    track_type_melody = sys.argv[2]
    threshold = float(sys.argv[3])
    csv_filename = sys.argv[4]
    path = sys.argv[5]
else:
    print """ ./multimodal.py <bass|melody> <melody|bass> <threshold> <csv_file> <path_to_files>
        <bass|melody>: tipo de pista que se va a seleccionar
        <melody|bass>: tipo de pista que aporta informacion
        <threshold>
        <csv_file>: fichero con las etiquetas
        <path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)
debug = False
#--------------------------------------------------------------------------------


# leemos el fichero csv
csv = lmidi.TCsv(csv_filename)
midi_list = {}
arff_list_bass = {}
arff_list_melody = {}
arff_header = ""
total_errors = {0:0, 1:0, 2:0, 3:0}
confusion_matrix = {'TP':0, 'FP':0, 'FN':0, 'TN':0}

# read all midi files and get the arff lines for each file
for filename in sorted(csv.dic.keys(), key=str.lower):
    m = lmidi.Midi(path+"/"+filename, True)
    midi_list[filename] = m
    midi_list[filename].gen_descriptors()
    # creacion de ficheros arff
    class_ok_bass = csv.get(filename, track_type_bass)
    class_ok_melody = csv.get(filename, track_type_melody)
    arff_list_bass[filename] = midi_list[filename].get_arff(class_ok_bass)
    arff_list_melody[filename] = midi_list[filename].get_arff(class_ok_melody)
    #print arff_list[filename]
    if not arff_header:
        arff_header = midi_list[filename].get_arff_header() + "\n"
    
# Leave one out
loo_list = leave_one_out(csv.get_files())

count = 0
# Create arff files and get error type for each file
for i in loo_list:
    midi_filename = i[0]
    create_arff_file(midi_filename,i[1])
    # fichero seleccionado
    m = midi_list[midi_filename]
    
    
    # ----- seleccion de la pista --------------------
    prob_bass = lmidi.get_probabilites("tmp/b_train.arff", "tmp/b_test.arff", debug)
    prob_melody = lmidi.get_probabilites("tmp/m_train.arff", "tmp/m_test.arff", debug)
    bass_track = get_track_multimodal(prob_bass, prob_melody, threshold, m)
    #print "---",midi_filename, bass_track
    error = csv.error(midi_filename, bass_track, track_type_bass)
    (TP, FP, FN, TN)  = csv.get_confusion_matrix(midi_filename, bass_track, track_type_bass)
    #print midi_filename, bass_track, error, (TP, FP, FN, TN)
    #print "---------------------"
    #print midi_filename,(TP, FP, FN, TN)
    total_errors[error] = total_errors[error] + 1
    confusion_matrix['TP'] = confusion_matrix['TP'] + TP
    confusion_matrix['FP'] = confusion_matrix['FP'] + FP
    confusion_matrix['FN'] = confusion_matrix['FN'] + FN
    confusion_matrix['TN'] = confusion_matrix['TN'] + TN
    count = count + 1
    if not count % 10:
        write_file("tmp/count.txt",str(count))
    



precision = lmidi.get_precision( confusion_matrix['TP'], confusion_matrix['FP'] )
recall = lmidi.get_recall( confusion_matrix['TP'], confusion_matrix['FN'] )
f_m = lmidi.get_f_measure( precision, recall)
accuracy = float(100*total_errors[0])/float(total_errors[0]+total_errors[1]+total_errors[2]+total_errors[3])

print "%s;%s;%.2f%%,%s;%s;%s;%s;%s;%s;%s;%s;%.2f;%.2f;%.2f" % (csv_filename.split("/")[-1], track_type_bass, accuracy, total_errors[0], total_errors[1], total_errors[2], total_errors[3], confusion_matrix['TP'], confusion_matrix['FP'], confusion_matrix['FN'],  confusion_matrix['TN'], precision, recall, f_m)




