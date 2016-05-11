#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint



def write_arff(arff_filename,content):
    f=open(arff_filename, "w")
    f.write(content)
    f.close()

#--------------------------------------------------

if( len(sys.argv)==3 ):
    print sys.argv[1], sys.argv[2]
    database=sys.argv[1]
    train=sys.argv[1]
    corpus=sys.argv[2]
else:
    print "Error en argumentos:\n./csp.py <train_arff_file> <corpus>"
    sys.exit(1)

debug=True





print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'

filename_list=os.listdir(corpus)
filename_list.sort()
for filename in filename_list:
    if debug:
        print "\n\n#-----------------------------------\nFile: ",filename
    m=lmidi.Tsmf2txt( corpus+"/"+filename)
    m.gen_descriptors()
    # arff fichero de validacion
    arff=m.get_arff_header('test')
    arff=arff+m.get_arff([])
    write_arff("/tmp/%s_%s.arff" % (corpus,filename) , arff)
    
    # Random Forest (weka)
    p=lmidi.get_probabilites(train,"/tmp/%s_%s.arff" % (corpus,filename), debug)
    # pista seleccionada
    s_ord=lmidi.select_track(p,0.01)
    if debug:
        print "Selected: " + str(s_ord)
    s=m.gno(s_ord[0])
    if s != -1:
        print '"%s",%s,,%s,,,,%s' % (filename, len(m.tracks.keys()), s, m.tracks[s].name)
    else:
        print '"%s",%s,,,,,,' % (filename, len(m.tracks.keys()))
    
    

