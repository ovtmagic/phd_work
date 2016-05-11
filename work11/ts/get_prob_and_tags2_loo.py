#!/usr/bin/python
#===============================================================================
# Crea un el fichero CSV con las pistas de bajo o melodia etiquetadas para todos
# los ficheros que hay en un directorio
#
# Utiliza el schema leave-one-out
#
# ./get_prob_and_tags2_loo.py <m_train_file.arff> <b_train_file.arff> <csv_file> <path_to_files>
#    <csv_file>: fichero con las etiquetas
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
#from lmidi import lmidi
import lmidi
from pprint import pprint

format_csv = False


#--------------------------------------------------------------------------------
# crea el fichero arff
def write_file(filename, content):
    f = open(filename, "w")
    f.write(content)
    f.close()

# crea los ficheros arff de train y test
def create_arff_file(one, all_files, arff_list):
    test_file = arff_header + arff_list[one]
    train_file = arff_header
    for i in all_files:
        train_file = train_file + arff_list[i] + "\n"
    write_file("tmp/test.arff",test_file)
    write_file("tmp/train.arff",train_file)

def leave_one_out(lista):
    result = []
    for one in lista:
        all_files=[]
        for i in lista:
            if i != one:
                all_files.append(i)
        result.append((one, all_files))
    return result
#--------------------------------------------------------------------------------




#--------------------------------------------------
if(len(sys.argv) == 3):
    #print sys.argv[1], sys.argv[2]
    csv_file_name = sys.argv[1]
    path = sys.argv[2]
else:
    print """ ./get_prob_and_tags2_loo.py <csv_file> <path_to_files>
        <csv_file>: fichero con las etiquetas
        <path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)

debug = False

if format_csv:
    print "Filename,num_track,prob_melody,prob_bass,prob_accomp,ocuppation,tag,track_label"
else:
    print "#################################################################################################################"
    print " Columnas:"
    print	" <numero pista>\t<prediccion>\t<prob melodia>\t<prob bajo>\t<prob accomp>\t<ocupacion>\t<etiquetado>\t<nombre de pista>"
    print "\nprediccion: tipo de pista que el algoritmo predice que es: +m para melodia, +b para bajo"
    print
    print "#################################################################################################################"
    print



# leemos el fichero csv
csv = lmidi.TCsv(csv_file_name)
midi_list = {}
m_arff_list = {}
b_arff_list = {}
a_arff_list = {}
arff_header = ""


# read all midi files and get the arff lines for each file
for filename in sorted(csv.dic.keys(), key=str.lower):
    m = lmidi.Midi(path+"/"+filename, True)
    midi_list[filename] = m
    midi_list[filename].gen_descriptors()
    m_class_ok = csv.get(filename, 'melody')
    b_class_ok = csv.get(filename, 'bass')
    a_class_ok = csv.get(filename, 'accomp')
    m_arff_list[filename] = midi_list[filename].get_arff(m_class_ok)
    b_arff_list[filename] = midi_list[filename].get_arff(b_class_ok)
    a_arff_list[filename] = midi_list[filename].get_arff(a_class_ok)
    #print arff_list[filename]
    if not arff_header:
        arff_header = midi_list[filename].get_arff_header() + "\n"
    
# Leave one out
loo_list = leave_one_out(csv.get_files())


# Para cada fichero midi crea los ficheros arff de train y test
# para melody, bajo y accomp
#for i in loo_list:
for i in [ x for x in loo_list if x[0] in ['Renaissance_Renaissance-Late_Victoria_Quam_Pulchri_Sunt-2-Gloria-c.mid','Medieval_ArsNova_Machau_machaut-b17.mid','Renaissance_Renaissance-Late_Victoria_Quicumque_Christum_Quaeritis-s.mid']]:
    midi_filename = i[0]
    m = midi_list[midi_filename]

    # Melody ---
    create_arff_file(midi_filename, i[1], m_arff_list)
    pm = lmidi.get_probabilites("tmp/train.arff", "tmp/test.arff", debug)
    # Bass ---
    create_arff_file(midi_filename, i[1], b_arff_list)
    pb = lmidi.get_probabilites("tmp/train.arff", "tmp/test.arff", debug)
    # Accomp ---
    create_arff_file(midi_filename, i[1], a_arff_list)
    pa = lmidi.get_probabilites("tmp/train.arff", "tmp/test.arff", debug)
    
    #---------------------------------------------------------------------------
    # en 'p' solo estan las pista validas, hay que crear p2 que contenga todas
    # las pistas (validas y no validas)
    #---------------------------------------------------------------------------
    # melody
    pm2 = {}
    for i in m.tracks.keys():
        pm2[i]=0.0
    for i in pm:
        pm2[m.gno(i)]=pm[i]
    #bass
    pb2 = {}
    for i in m.tracks.keys():
        pb2[i]=0.0
    for i in pb:
        pb2[m.gno(i)]=pb[i]
    #accomp
    pa2 = {}
    for i in m.tracks.keys():
        pa2[i]=0.0
    for i in pa:
        pa2[m.gno(i)]=pa[i]
    #---------------------------------------------------------------------------
    #print p
    if not format_csv:
        print "* ",midi_filename
    for t in m.tracks.keys():
        # probabilidad de que la pista sea bajo (o melodia)
        selected = ""
        prob_track_m = pm2[t]
        prob_track_b = pb2[t]
        prob_track_a = pa2[t]
        selected = ""
        if prob_track_m >= 0.5:
            selected = selected + "m"
        if prob_track_b >= 0.5:
            selected = selected + "b"
        if prob_track_a >= 0.5:
            selected = selected + "a"
        if selected:
            selected = "+" + selected
        
        oc=""
        if m.tracks[t].is_valid():
            oc=str(round(m.tracks[t]._get_occupation_rate(),2))
            prob_track_m=round(prob_track_m, 1)
            prob_track_b=round(prob_track_b, 1)
            prob_track_a=round(prob_track_a, 1)
        else:
            prob_track_m=""
            prob_track_b=""
            prob_track_a=""
        tag = csv.get_tag_by_track(midi_filename, t) or ""
        #if not oc and tag:
        if format_csv:
            if m.tracks[t].is_valid():
                print "%s,%s,%s,%s,%s,%s,%s,%s" % (midi_filename, t, prob_track_m, prob_track_b, prob_track_a, oc, tag, m.tracks[t].name)
        else:
            print "   %2s   %4s   %3s   %3s   %3s  %4s %-9s  %s" % (t, selected, prob_track_m, prob_track_b, prob_track_a, oc, tag, m.tracks[t].name)
        
    if not format_csv:
        print "\n\n%----------------------------------\n"
    """
    # pista seleccionada
    s_ord=lmidi.select_track(p,0.01)
    if debug:
        print "Selected: " + str(s_ord)
    s=m.gno(s_ord[0])
    if s != -1:
        # se debe comentar una de las lineas siguietes segun se este obteniendo
        # el csv para bajo o para melodia 
        # para melodia
        print '"%s",%s,%s,,,,,%s' % (filename, len(m.tracks.keys()), s, m.tracks[s].name)
        # para bajo
        #print '"%s",%s,,%s,,,,%s' % (filename, len(m.tracks.keys()), s, m.tracks[s].name)
    else:
        print '"%s",%s,,,,,,' % (filename, len(m.tracks.keys()))
    """
    


