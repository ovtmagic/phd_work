#!/usr/bin/python
#===============================================================================
# Obtiene los atributos de los ficheros midi de uno o varios directorios
# 
# ./get_attr.py <csv file> <dir>
#    <csv file>: fichero csv con el etiquetado
#    <dir>: directorio con los ficheros MIDI
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
    csvfile = sys.argv[1]
    path = sys.argv[2]
else:
    print "Error en argumentos:\n./get_attr.py <csv file> <path_to_files>"
    sys.exit(1)

debug = False





#print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'

# Checks if paht is a directory or a MIDI file
if os.path.isdir(path):
    filename_list=os.listdir(path)
    filename_list.sort()
else:
    filename_list = [path]

# leemos el fichero csv
csv = lmidi.TCsv(csvfile)
    
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
    
    
    #---------------------------------------------------------------------------
    #print p
    for t in m.tracks.keys():
        # se obtiene el atributo
        attr=0.0
        if m.tracks[t].is_valid():
            attr=round(m.tracks[t]._get_occupation_rate(),2)
        # se obtiene la etiqueta
        tag = csv.get_tag_by_track(filename, t) or "NULL"
        print "%s;%s;%s;%s;%s" % (filename,t,tag,attr,m.tracks[t].name)
    #print csv.get(filename,'bass')
        
        

