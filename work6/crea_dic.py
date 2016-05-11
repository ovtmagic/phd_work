#!/usr/bin/python
#===============================================================================
# Crea un diccionario con las etiquetas que son melodia.
# -- Creo que esto al final no se ha usado --
#===============================================================================
import sys
import os
import lmidi
from pprint import pprint

path = "/tmp/mir/clasica/"
csv_file = "clasica.csv"


def parse(cad):
    cad_parsed = cad.lower().replace(" ", "")
    return cad_parsed


#===============================================================================
# Se obtienen los nombres de todas las pistas MIDI y se clasifican como
# melodia o no_melodia
#===============================================================================

melody_labels = []
no_melody_labels = []

# cargamos el fichero csv
csv = lmidi.TCsv(csv_file)

filename_list = os.listdir(path)[:10]
filename_list.sort()
#filename_list=["Ana_Maria.MID"]
for filename in sorted(filename_list, key=str.lower):
    print "*", filename
    m = lmidi.Midi()
    m.load_midi(path + filename)
    m.load_skyline(path + filename)
    
    melody_tracks = csv.get(filename, "melody")
    # se comprueban todas las etiquetas
    for i in  m.tracks.keys():
        if m.tracks[i].is_valid():
            # si la etiqueta es valida se quitan caractares especiales y se
            # deja en minusculas
            label = parse(m.tracks[i].name)
            if i in melody_tracks:
                if label not in melody_labels:
                    melody_labels.append(label)
            else:
                if label not in no_melody_labels:
                    no_melody_labels.append(label)
                    
melody_labels.sort()
no_melody_labels.sort()

#===============================================================================
# Se crean los ficheros melody.dic (con las etiquetas que son melodia) y
# no_melody.dic (con las etiquetas que no son melodia). Es posible que una
# misma etiqueta este en los dos ficheros (es melodia en un fichero midi pero
# no en otro)
#===============================================================================

f = open('melody.dic', 'w')
for i in melody_labels:
    f.write(i + "\n")
f.close()
