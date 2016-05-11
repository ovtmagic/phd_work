#!/usr/bin/python
#-----------------------------------------------------------
# Crea un fichero csv con el campo 'accomp' que contiene las
# pistas de acomanamiento. Estas pistas son todas las pistas
# que no son ni bajo ni melodia
#-----------------------------------------------------------


import sys
from lmidi import lmidi
from pprint import pprint



def array_to_str(v):
    s = ''
    for i in v:
        if s:
            s = "%s %s" % (s,i)
        else:
            s = "%s" % i
    return s



if( len(sys.argv) != 2):
    print "Error:"
    print "./extend_csv.py <path_to_files>\n"
    sys.exit(1)
csv_filename = sys.argv[1]



print '"Nombre_fichero",N_Pistas,melody,bass,piano_rh,piano_lh,mixdown,accomp'

# leemos el fichero csv
csv = lmidi.TCsv(csv_filename)

for fname in sorted(csv.dic.keys(), key=str.lower):
    #print fname
    #pprint(csv.dic[fname])
    bass_melody_tracks = csv.get(fname, 'bass') + csv.get(fname, 'melody')
    other_tracks = []
    for i in range(1, csv.get_num_tracks(fname)+1):
        if not i in bass_melody_tracks:
            other_tracks.append(i)
    """
    print "-----------"
    print " >>>", csv.get_num_tracks(fname)
    print " >", array_to_str(bass_melody_tracks)
    print " >", array_to_str(other_tracks)
    print "-----------\n\n\n"
    """
    print "%s,%s,%s,%s,%s,%s,%s,%s" % (
                fname,
                csv.get_num_tracks(fname),
                array_to_str(csv.get(fname, 'melody')),
                array_to_str(csv.get(fname, 'bass')),
                array_to_str(csv.get(fname, 'piano_rh')),
                array_to_str(csv.get(fname, 'piano_lh')),
                array_to_str(csv.get(fname, 'mixdown')),
                array_to_str(other_tracks),
    )