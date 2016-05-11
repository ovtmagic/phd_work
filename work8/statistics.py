#!/usr/bin/python
#===============================================================================
# Crea un el fichero CSV con las pistas de bajo o melodia etiquetadas para todos
# los ficheros que hay en un directorio
#
# ./statistics.py <bass|melody> <csv_file> <path_to_files>
#    <bass|melody>
#    <csv_file>: fichero con las etiquetas
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
if(len(sys.argv) == 4):
    track_type = sys.argv[1]
    csv_file_name = sys.argv[2]
    path = sys.argv[3]
else:
    print """ ./statistics.py <bass|melody> <csv_file> <path_to_files>
        <bass|melody>
        <csv_file>: fichero con las etiquetas
        <path_to_files>: directorio con los ficheros MIDI"""
    sys.exit(1)

debug = False


# listado de etiquetas y numero de veces que aparece cada etiqueta de tipo bass|melody
class_labels = {}
# listado de etiquetas y numero de veces que aparece cada etiqueta de cualquier tipo
labels = {}
# numero de pistas validas
num_tracks = 0
# numero de pistas class (class=bass|melody)
num_tracks_class = 0
num_tracks_no_class = 0
# ficheros midi con 0, 1 o mas de 1 "class" track
numfiles_0_class = 0
numfiles_1_class = 0
numfiles_x_class = 0


# leemos el fichero csv
csv = lmidi.TCsv(csv_file_name)

for filename in sorted(csv.dic.keys(), key=str.lower):
    if debug:
        print "\n\n#-----------------------------------\nFile: ",filename
    m=lmidi.Midi(path+"/"+filename, True)
    m.gen_descriptors()
    
    #print p
    #print "* ",filename
    for t in m.tracks.keys():
        if m.tracks[t].is_valid():
            num_tracks = num_tracks + 1
            if t in csv.get(filename, track_type):
                num_tracks_class = num_tracks_class + 1
            else:
                num_tracks_no_class = num_tracks_no_class + 1
                
            track_label = unicode(m.tracks[t].name.lower(), errors='ignore')
            # contamos todas las etiquetas
            if track_label:
                if track_label in labels.keys():
                    labels[track_label] = labels[track_label] +1
                else:
                    labels[track_label] = 1
            # contamos las etiquetas de bajo o melodia
            if track_label and t in csv.get(filename, track_type):
                if track_label in class_labels.keys():
                    class_labels[track_label] = class_labels[track_label] +1
                else:
                    class_labels[track_label] = 1
    # se cuentas los ficheros con 0, 1 o mas pistas "class"
    if not csv.get(filename, track_type):
        numfiles_0_class = numfiles_0_class +1
    elif len(csv.get(filename, track_type)) == 1:
        numfiles_1_class = numfiles_1_class +1
    else:
        numfiles_x_class = numfiles_x_class +1

    """
    print "-,Num tracks,%s" % num_tracks
    print "-,Num %s tracks,%s" % (track_type, num_tracks_class)
    print "-,Num no %s tracks,%s" % (track_type, num_tracks_no_class)
    print csv.get(filename, track_type)
    print "\n\n%----------------------------------\n"
    """


# Imprime resultados
print "-,Num tracks,%s" % num_tracks
print "-,Num %s tracks,%s" % (track_type, num_tracks_class)
print "-,Num no %s tracks,%s" % (track_type, num_tracks_no_class)
print "-,Diferent all tags,%s" % len(labels.keys())
print "-,Diferent %s tags,%s" % (track_type, len(class_labels.keys()))
print "-,Files with 0 %s tracks,%s" % (track_type, numfiles_0_class)
print "-,Files with 1 %s tracks,%s" % (track_type, numfiles_1_class)
print "-,Files with more than 1 %s tracks,%s" % (track_type, numfiles_x_class)
print "-,Total files,%s" % len(csv.dic.keys())

print "\n\n"
"""
for i in class_labels.keys():
    print "%s,%s" % (class_labels[i], i)
"""