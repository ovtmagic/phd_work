#!/usr/bin/python
#===============================================================================
# Crea un el fichero CSV con las pistas de bajo o melodia etiquetadas para todos
# los ficheros que hay en un directorio
#
# ./crea_csv.py <train_file.arff> <path_to_files>
#    <train_file.arff>: fichero de weka que se utiliza para entrenar el algoritmo
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
import lmidi
from pprint import pprint



def write_arff(arff_filename,content):
    f=open(arff_filename, "w")
    f.write(content)
    f.close()

#--------------------------------------------------
if( len(sys.argv)==4 ):
    #print sys.argv[1], sys.argv[2]
    track_type=sys.argv[1]
    train=sys.argv[2]
    path=sys.argv[3]
    if track_type not in ('melody', 'bass'):
        print "Error en argumentos:\n./csp.py <melody|bass> <train_arff_file> <corpus_name> <path_to_files>"
        sys.exit(1)
else:
    print "Error en argumentos:\n./csp.py <melody|bass> <train_arff_file> <path_to_files>"
    sys.exit(1)

# If debug=True weka logs are printed
debug=False





print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'

filename_list=os.listdir(path)
filename_list.sort()
for filename in sorted(filename_list, key=str.lower):
    if debug:
        print "\n\n#-----------------------------------\nFile: ",filename
    m=lmidi.Midi()
    m.load_midi(path+"/"+filename)
    m.load_skyline(path+"/"+filename)
    m.gen_descriptors()
    # arff fichero de test
    arff=m.get_arff_header('test')
    arff=arff+m.get_arff([])
    write_arff("/tmp/%s.arff" % (filename) , arff)
    
    # Random Forest (weka)
    p=lmidi.get_probabilites(train,"/tmp/%s.arff" % (filename), debug)
    # pista seleccionada
    s_ord=lmidi.select_track(p,0.01)
    if debug:
        print "Selected: " + str(s_ord)
    s=m.gno(s_ord[0])
    if s != -1:
        # se debe comentar una de las lineas siguietes segun se este obteniendo
        # el csv para bajo o para melodia 
        # para melodia
        if track_type == 'melody':
            print '"%s",%s,%s,,,,,%s' % (filename, len(m.tracks.keys()), s, m.tracks[s].name)
        # para bajo
        else:
            print '"%s",%s,,%s,,,,%s' % (filename, len(m.tracks.keys()), s, m.tracks[s].name)
    else:
        print '"%s",%s,,,,,,' % (filename, len(m.tracks.keys()))
    
    


