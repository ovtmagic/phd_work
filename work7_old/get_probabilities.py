#!/usr/bin/python
#===============================================================================
# Crea un el fichero CSV con las pistas de bajo o melodia etiquetadas para todos
# los ficheros que hay en un directorio
#
# ./crea_csv.py <train_file.arff> <corpus_name> <path_to_files>
#    <train_file.arff>: fichero de weka que se utiliza para entrenar el algoritmo
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
import lmidi
from pprint import pprint



def write_arff(arff_filename, content):
    f = open(arff_filename, "w")
    f.write(content)
    f.close()

#--------------------------------------------------
if(len(sys.argv) == 3):
    #print sys.argv[1], sys.argv[2]
    train = sys.argv[1]
    path = sys.argv[2]
else:
    print "Error en argumentos:\n./csp.py <train_arff_file> <path_to_files>"
    sys.exit(1)

debug = False





#print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'

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
    filename_arff = "./tmp/%s.arff" % filename.replace("/","")
    write_arff(filename_arff, arff)
    
    # Random Forest (weka)
    p=lmidi.get_probabilites(train, filename_arff, debug)
    #---------------------------------------------------------------------------
    # en 'p' solo estan las pista validas, hay que crear p2 que contenga todas
    # las pistas (validas y no validas)
    #---------------------------------------------------------------------------
    p2 = {}
    for i in m.tracks.keys():
        p2[i]=0.0
    for i in p:
        p2[m.gno(i)]=p[i]
    #---------------------------------------------------------------------------
    #print p
    print "* ",filename
    for t in m.tracks.keys():
        # probabilidad de que la pista sea bajo (o melodia)
        selected = " "
        prob_track = p2[t]
        if prob_track >= 0.5:
            selected = "+"
        oc="    "
        if m.tracks[t].is_valid():
            oc=str(round(m.tracks[t]._get_occupation_rate(),2))
        else:
            prob_track="    "
        print "   %2s   %s   %s  %s\t %s" % (t, selected, prob_track, oc,m.tracks[t].name)
        
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
    


