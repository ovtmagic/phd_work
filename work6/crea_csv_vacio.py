#!/usr/bin/python
#===============================================================================
# Crea un el fichero CSV vacio para etiquetar las pistas de bajo o melodia
# los ficheros que hay en un directorio
#
# ./crea_csv.py <path_to_files>
#    <path_to_files>: directorio con los ficheros MIDI
#===============================================================================
import sys
import os
import lmidi
from pprint import pprint




#--------------------------------------------------
if( len(sys.argv)==2):
    #print sys.argv[1], sys.argv[2]
    path=sys.argv[1]
else:
    print "Error en argumentos:\n./crea_csv_vacio.py  <path_to_files>"
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
    #m.gen_descriptors()
    print '"%s",%s,,,,,,' % (filename, len(m.tracks.keys()))
    
    


