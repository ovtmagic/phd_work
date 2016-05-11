#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint


def write_arff(arff_filename,content):
    f=open(arff_filename, "w")
    f.write(content)
    f.close()


train="b_clas200.arff"
corpus="clas200"


print '"Nombre_fichero","N_Pistas","melody","bass",piano_rh,"piano_lh","mixdown"'

filename_list=os.listdir(corpus)
filename_list.sort()
csv=lmidi.TCsv(corpus+".csv")

for filename in filename_list:
    #print ">>>>>",filename
    m=lmidi.Tsmf2txt( corpus+"/"+filename)
    tracks_ok=csv.get(filename,'bass')
    
    track_name=""
    if tracks_ok:
        track_name=m.tracks[tracks_ok[0]].name
    
    
    if tracks_ok:
        print '"%s",%s,,%s,,,,%s' % (filename, len(m.tracks.keys()), tracks_ok[0], track_name)
    else:
        print '"%s",%s,,,,,,' % (filename, len(m.tracks.keys()))
    
    

