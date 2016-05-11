#!/usr/bin/python
#===============================================================================
# Crea un el fichero CSV con las pistas de bajo o melodia etiquetadas para todos
# los ficheros que hay en un directorio
#
# ./get_prob_and_tags.py <m_train_file.arff> <b_train_file.arff> <csv_file> <path_to_files>
#    <m_train_file.arff>: fichero de weka entrenado con melodia
#    <b_train_file.arff>: fichero de weka entrenado con bajo
#    <csv_file>: fichero con las etiquetas
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
import lmidi
#import cyg_lmidi as lmidi
from pprint import pprint



def write_arff(arff_filename, content):
    f = open(arff_filename, "w")
    f.write(content)
    f.close()

#--------------------------------------------------
if(len(sys.argv) == 5):
    #print sys.argv[1], sys.argv[2]
    train_m = sys.argv[1]
    train_b = sys.argv[2]
    csv_file_name = sys.argv[3]
    path = sys.argv[4]
else:
    print """ ./get_prob_and_tags.py <m_train_file.arff> <b_train_file.arff> <csv_file> <path_to_files>
			<m_train_file.arff>: fichero de weka entrenado con melodia
			<b_train_file.arff>: fichero de weka entrenado con bajo
			<csv_file>: fichero con las etiquetas
			<path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)

debug = False



print "#################################################################################################################"
print " Columnas:"
print	" <numero pista>\t<prediccion>\t<prob melodia>\t<prob bajo>\t<ocupacion>\t<etiquetado>\t<nombre de pista>"
print "\nprediccion: tipo de pista que el algoritmo predice que es: +m para melodia, +b para bajo"
print
print "#################################################################################################################"
print


#print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'


# leemos el fichero csv
csv = lmidi.TCsv(csv_file_name)

# Checks if paht is a directory or a MIDI file
if os.path.isdir(path):
    filename_list=os.listdir(path)
    filename_list.sort()
else:
    filename_list = [path]
    
for filename in sorted(filename_list, key=str.lower):
    if debug:
        print "\n\n#-----------------------------------\nFile: ",filename
    m=lmidi.Midi()
    # checks if path is a directory or a MIDI file
    if os.path.isdir(path):
        m.load_midi(path+"/"+filename)
        m.load_skyline(path+"/"+filename)
    else:
        m.load_midi(filename)
        m.load_skyline(filename)
    m.gen_descriptors()
    # arff fichero de test
    arff=m.get_arff_header('test')
    arff=arff+m.get_arff([])
    filename_arff = "/tmp/%s.arff" % filename.replace("/","")
    write_arff(filename_arff, arff)
    
    # Random Forest (weka)
    # prob melodia
    pm=lmidi.get_probabilites(train_m, filename_arff, debug)
    # prob bajo
    pb=lmidi.get_probabilites(train_b, filename_arff, debug)
    #---------------------------------------------------------------------------
    # en 'p' solo estan las pista validas, hay que crear p2 que contenga todas
    # las pistas (validas y no validas)
    #---------------------------------------------------------------------------
    pm2 = {}
    for i in m.tracks.keys():
        pm2[i]=0.0
    for i in pm:
        pm2[m.gno(i)]=pm[i]
    pb2 = {}
    for i in m.tracks.keys():
        pb2[i]=0.0
    for i in pb:
        pb2[m.gno(i)]=pb[i]
    #---------------------------------------------------------------------------
    #print p
    print "* ",filename
    for t in m.tracks.keys():
        # probabilidad de que la pista sea bajo (o melodia)
        selected = ""
        prob_track_m = pm2[t]
        prob_track_b = pb2[t]
        if prob_track_m >= 0.5:
            selected = "+m"
        if prob_track_b >= 0.5:
            selected = "+b"
        oc=""
        if m.tracks[t].is_valid():
            oc=str(round(m.tracks[t]._get_occupation_rate(),2))
        else:
            prob_track_m=""
            prob_track_b=""
        tag = csv.get_tag_by_track(filename, t) or ""
        #if not oc and tag:
        print "   %2s   %2s   %3s   %3s  %4s %-9s  %s" % (t, selected, prob_track_m, prob_track_b, oc, tag, m.tracks[t].name)
        
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
    


