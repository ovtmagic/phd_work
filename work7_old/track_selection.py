#!/usr/bin/python
#===============================================================================
# Obtiene las estadisticas y tipo de error en la seleccion de la pista de bajo
# o melodia de un listado de ficheros midi
#
# ./track_selection.py <bass|melody> <threshold> <train_file.arff> <csv_file> <path_to_files>
#    <bass|melody>
#    <threshold>
#    <train_file.arff>: fichero de weka de entrenamiento
#    <csv_file>: fichero con las etiquetas
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
import lmidi
from pprint import pprint

# Variables globales
read_from_csv = True
show_individual_results = False
debug = False


def write_file(arff_filename, content):
    f = open(arff_filename, "w")
    f.write(content)
    f.close()

#--------------------------------------------------

if (len(sys.argv) == 2 and sys.argv[1] == "header"):
    print "Train Filename;Test Filename;track type;Acc.%Error 0;Error 1;Error 2;Error 3;TP;FP;FN;TN;Precision;Recall;F-measure"
    sys.exit(0)


if(len(sys.argv) == 6):
    #print sys.argv[1], sys.argv[2]
    track_type = sys.argv[1]
    threshold = float(sys.argv[2])
    train_filename = sys.argv[3]
    csv_filename = sys.argv[4]
    path = sys.argv[5]
else:
    print """ ./track_selection.py <bass|melody> <threshold> <train_file.arff> <b_train_file.arff> <csv_file> <path_to_files>
        <bass|melody>
        <threshold>
        <train_file.arff>: fichero de weka de entrenamiento
        <csv_file>: fichero con las etiquetas
        <path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)






# leemos el fichero csv
csv = lmidi.TCsv(csv_filename)

# Checks if paht is a directory or a MIDI file
if read_from_csv:
    filename_list = sorted(csv.dic.keys(), key=str.lower)
else:
    filename_list = os.listdir(path)
    filename_list.sort()

total_error = {0:0, 1:0, 2:0, 3:0}
confusion_matrix = {'TP':0, 'FP':0, 'FN':0, 'TN':0}

#for filename in sorted(filename_list, key=str.lower):
for filename in filename_list:
    if debug:
        print "\n\n#-----------------------------------\nFile: ",filename
    m = lmidi.Midi(path+"/"+filename, True)
    m.gen_descriptors()
    
    # arff fichero de test -----------------
    arff=m.get_arff_header('test')
    arff=arff+m.get_arff([])
    test_filename = "./tmp/%s.arff" % filename.replace("/","")
    write_file(test_filename, arff)
    
    # Random Forest (weka) -----------------
    prob = lmidi.get_probabilites(train_filename, test_filename, debug)
    selected_track = m.get_selected_track(train_filename, test_filename, threshold, prob)
    # get errors and confusion matrix
    error = m.get_selected_error(track_type, train_filename, threshold, csv, prob)
    (TP, FP, FN, TN) = m.get_confusion_matrix(track_type, train_filename, threshold, csv, prob)
    total_error[error] = total_error[error] + 1
    #print filename, (TP, FP, FN, TN)
    confusion_matrix['TP'] = confusion_matrix['TP'] + TP
    confusion_matrix['FP'] = confusion_matrix['FP'] + FP
    confusion_matrix['FN'] = confusion_matrix['FN'] + FN
    confusion_matrix['TN'] = confusion_matrix['TN'] + TN
    #
    if show_individual_results:
        success=error1=error2=error3=0
        if error == 0:
            success = 1
        elif error == 1:
            error1 = 1
        elif error == 2:
            error2 = 1
        elif error == 3:
            error3 = 1
        print "%s,%s,%s,%s,%s,%s,%s" % (filename, track_type, selected_track, success, error1, error2, error3)
    if debug:
        print "\n\n%----------------------------------\n"
    

precision = lmidi.get_precision( confusion_matrix['TP'], confusion_matrix['FP'] )
recall = lmidi.get_recall( confusion_matrix['TP'], confusion_matrix['FN'] )
f_m = lmidi.get_f_measure( precision, recall)

accuracy = float(100*total_error[0])/float(total_error[0]+total_error[1]+total_error[2]+total_error[3])
#print "Total:",total_error
#print "Total %s / %s,%s,%s,%s,%s,%s,%s" % (train_filename,csv_filename, track_type, selected_track, error[0], error[1], error[2], error[3])
print "Total %s,%s,%s,%s,%.2f%%,%s,%s,%s,%s,%s,%s,%s,%s,%.2f,%.2f,%.2f" % (train_filename.split("/")[-1],csv_filename.split("/")[-1], 
    track_type, " ", accuracy, total_error[0], total_error[1], total_error[2], total_error[3],
    confusion_matrix['TP'], confusion_matrix['FP'], confusion_matrix['FN'],  confusion_matrix['TN'], precision, recall, f_m)
