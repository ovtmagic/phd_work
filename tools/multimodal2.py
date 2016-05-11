#!/usr/bin/python
#===============================================================================
# Seleccion bajo/melodia utilizando utilizando la infomacion proporcionada por
# el conocimiento de la otra pista (melodia/bajo)
#
# Se utiliza una base de datos "train", y se selecciona la pista sobre la base de
# datos "test"
#
# ./multimodal.py <bass|melody> <threshold > <bass arff train file >  <melody arrf train file> <csv_file> <path_to_files>
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
    # a saco - para la pista 0 se sobreescribe P(i|M)=0, de manera que p(i|B)(1-p(i|M))=p(i|B)
    # por tanto la pista 0 puede ser de bajo y de melodia
    prob_iM[-1] = 0.0
    # se obtiene el vector "multimodal" iB
    iB = {}
    for i in prob_iB.keys():
        iB[i] = prob_iB[i]*(1.0-prob_iM[i])
    #x = 0.0
    #for i in prob_iB.keys():
    #    x = x + prob_iB[i]
    # Se busca la pista que maximiza iB
    max_prob_iB = 0.0
    max_i = -1
    for i in iB.keys():
        #print "        >>>>>>>",i,iB[i],max_prob_iB, iB[i] >= max_prob_iB
        if iB[i] >= max_prob_iB:
            max_prob_iB = iB[i]
            max_i = i
    # devuele el numero de pista real en el fichero midi
    """
    print prob_bass
    print prob_melody
    print prob_iB
    print prob_iM
    print "iB",max_prob_iB
    print "prob iB",max_i,m.gno(max_i)
    print iB
    """
    return m.gno(max_i)
    
    
    






#--------------------------------------------------------------------------------
# crea el fichero arff
def write_file(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()


 
#--------------------------------------------------------------------------------
if (len(sys.argv) == 2 and sys.argv[1] == "header"):
    print "Filename;track type;Acc.%;Error 0;Error 1;Error 2;Error 3;TP;FP;FN;TN;Precision;Recall;F-measure"
    sys.exit(0)
    
if (len(sys.argv) == 8):
    # se selecciona esta pista (bass)
    track_type_bass = sys.argv[1]
    # teniendo en cuenta la informacion de esta pista (melody)
    track_type_melody = sys.argv[2]
    threshold = float(sys.argv[3])
    bass_train_file = sys.argv[4]
    melody_train_file = sys.argv[5]
    csv_filename = sys.argv[6]
    path = sys.argv[7]
else:
    print """ ./multimodal.py <bass|melody> <melody|bass> <threshold> <csv_file> <path_to_files>
        <bass|melody>: tipo de pista que se va a seleccionar
        <melody|bass>: tipo de pista que aporta informacion
        <threshold>
        <arff bass train file>
        <arff melody train file>
        <csv_file>: fichero con las etiquetas
        <path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)
debug = False
#--------------------------------------------------------------------------------


# leemos el fichero csv
csv = lmidi.TCsv(csv_filename)
arff_header = ""
total_errors = {0:0, 1:0, 2:0, 3:0}
confusion_matrix = {'TP':0, 'FP':0, 'FN':0, 'TN':0}

count = 0
# read all midi files and get the arff lines for each file
for filename in sorted(csv.dic.keys(), key=str.lower):
    m = lmidi.Midi(path+"/"+filename, True)
    m.gen_descriptors()
    
    # arff fichero de test -----------------
    arff=m.get_arff_header('test')
    arff=arff+m.get_arff([])
    test_filename = "./tmp/%s.arff" % filename.replace("/","")
    write_file(test_filename, arff)

    # ----- seleccion de la pista --------------------
    #print ">>>>",bass_train_file, test_filename
    prob_bass = lmidi.get_probabilites(bass_train_file, test_filename, debug)
    prob_melody = lmidi.get_probabilites(melody_train_file, test_filename, debug)
    
    bass_track = get_track_multimodal(prob_bass, prob_melody, threshold, m)
    
    #print "---",midi_filename, bass_track
    error = csv.error(filename, bass_track, track_type_bass)
    (TP, FP, FN, TN)  = csv.get_confusion_matrix(filename, bass_track, track_type_bass)
    #print midi_filename, bass_track, error, (TP, FP, FN, TN)
    #print "---------------------"
    #print filename,(TP, FP, FN, TN)
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

print "%s;%s;%.2f;%s;%s;%s;%s;%s;%s;%s;%s;%.2f;%.2f;%.2f" % (csv_filename.split("/")[-1], track_type_bass, accuracy, total_errors[0], total_errors[1], total_errors[2], total_errors[3], confusion_matrix['TP'], confusion_matrix['FP'], confusion_matrix['FN'],  confusion_matrix['TN'], precision, recall, f_m)




