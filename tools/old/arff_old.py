#!/usr/bin/python

import sys
import os
import lmidi
from pprint import pprint



tracktype="bass"
corpus="jazz200"

csvfile="%s.csv" % corpus
csv=lmidi.TCsv(csvfile)


arff=""

# Check all files into a path
midifiles={}

for filename in os.listdir(corpus):
    class_ok=csv.get(filename,tracktype)
    #print filename, class_ok
    
    m=lmidi.Tsmf2txt( corpus+"/"+filename)
    m.gen_descriptors()
    
    if not arff:
        arff=m.get_arff_header(tracktype+"_"+corpus)
    arff=arff+m.get_arff( class_ok )
    
print arff
    