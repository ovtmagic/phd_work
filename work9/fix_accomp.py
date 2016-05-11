#!/usr/bin/python
#-----------------------------------------------------------
# Elimina la etiqueta 'accomp' de las pistas no validas
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



if( len(sys.argv) != 3):
    print "Error:"
    print "./fix_accomp.py <csv_file> <path_to_midi_files>\n"
    sys.exit(1)
csv_filename = sys.argv[1]
path = sys.argv[2]



print '"Nombre_fichero",N_Pistas,melody,bass,piano_rh,piano_lh,mixdown,accomp'

# leemos el fichero csv
csv = lmidi.TCsv(csv_filename)


for fname in sorted(csv.dic.keys(), key=str.lower):
    m = lmidi.Midi(path+"/"+fname, True)
    #print fname
    #pprint(csv.dic[fname])
    #bass_melody_tracks = csv.get(fname, 'bass') + csv.get(fname, 'melody')
    new_accomp_tracks = []
    for i in csv.get(fname, 'accomp'):
        #print i,m.tracks[i].is_valid()
        if m.tracks[i].is_valid():
            new_accomp_tracks.append(i)
        
    """
    print "\n\n\n-----------"
    print " >>>", csv.get_num_tracks(fname)
    #print " >", array_to_str(bass_melody_tracks)
    print " >", csv.get(fname, 'accomp')
    print " >", array_to_str(new_accomp_tracks)
    print "-----------"
    """
    print "%s,%s,%s,%s,%s,%s,%s,%s" % (
                fname,
                csv.get_num_tracks(fname),
                array_to_str(csv.get(fname, 'melody')),
                array_to_str(csv.get(fname, 'bass')),
                array_to_str(csv.get(fname, 'piano_rh')),
                array_to_str(csv.get(fname, 'piano_lh')),
                array_to_str(csv.get(fname, 'mixdown')),
                array_to_str(new_accomp_tracks),
    )