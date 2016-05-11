#!/usr/bin/python

import sys
import os
import lmidi
from pprint import pprint






# Leave One Out -----------------------------------------------------------
def write_arff(arff_filename,content):
    f=open(arff_filename, "w")
    f.write(content)
    f.close()


def loo(midifiles,csv,thres=0.25):
    midifiles_keys=midifiles.keys()
    # se calcula el fichero arff para todos los ficheros midi
    arff={}
    arff_header=""
    #print "0>"
    for i in midifiles_keys:
        arff[i]=midifiles[i].get_arff( csv.get(i,type_file) )
        if not arff_header:
            arff_header = midifiles[i].get_arff_header("leave_one_out")
    result={}
    count=1
    #print "Empezando"
    for i in midifiles_keys:
        #print "Test midifile:\t%s (%s)" % (i,count) #+" "+midifiles[i].filename
        count = count +1
        arff_test = arff_header + arff[i]
        arff_train = arff_header
        #print "A>"
        for j in midifiles_keys:
            if j !=i:
                arff_train = arff_train + arff[j]
        #print "B>"
        test_filename="/tmp/"+i+".test.arff"
        train_filename="/tmp/"+i+".train.arff"
        write_arff(test_filename, arff_test)
        write_arff(train_filename, arff_train)
        
        #print "C>"
        probabilities=lmidi.get_probabilites(train_filename, test_filename, False)
        (t,p)=lmidi.select_track(probabilities, thres)
        result[i]=t
        #print "D>"
        
    return result

# Experimento 2--------------------------------------------------
def exp_2(midifiles,dirpath):
    latex="&   Dataset  &  Success & Error Tipo 1 & Error Tipo 2 &  Error Tipo 3 \\\\"
    # LOO
    for path in dirpath:
        #print "Dataset: ",path
        csv = lmidi.TCsv(path+".csv")
        errores=[0,0,0,0]
        count=0
        x=loo(midifiles[path],csv,umbral)  # { file_name:track, file_name:track, ....}
    
        for i in x.keys():
            name=i
            track_ord=x[i]
            track_num=midifiles[path][i].get_numbyord(track_ord)
            error = csv.error(name, track_num,type_file)
            #print "Select midifile: %s\t\t%s (%s),%s"  % (name,track_num,track_ord,error  )
            errores[error] += 1
            count += 1
        latex=latex+"\n"+"%s \t&\t %.1f \t&\t %s \t&\t %s \t&\t \%s \t \\\\" % (path,100.0*errores[0]/count, errores[1],errores[2],errores[3])
        
    return latex

#-------------------------------------------------------------

# Corpus y tipo de pista (bajo, melodia, etc...)
dirpath=["kar200","jazz200","clas200"]
#dirpath=["test","test2"]


umbral=0.25
# contabilizacion de errores (tipo 1, 2 y 3. no error=0)

midifiles={}    # dic con los ficheros midi-smf


# Search into all paths or sets
for path in dirpath:
    # Check all files into a path
    midifiles[path]={}
    for filename in os.listdir(path):
        midifiles[path][filename]=lmidi.Tsmf2txt( path+"/"+filename)
        midifiles[path][filename].gen_descriptors()




type_file='bass'
print "CLASS:",type_file
print exp_2(midifiles,dirpath)
print
print

type_file='melody'
print "CLASS:",type_file
print exp_2(midifiles,dirpath)
print
print
    
