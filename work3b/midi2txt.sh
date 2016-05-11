#!/bin/bash

cd /tmp/mir
#smf2txt="/Users/octavio/bin/smf2txt"
smf2txt="/usr/local/bin/smf2txt"
#/Users/octavio/bin/smf2txt -f "%p %o %d %v %c" -p 1 clasica/allemande_otra.mid

# directorios con los corpus
for d in `ls|grep -v txt`
do
    echo "+ Creando " $d
    new_d="txt/${d}"
    mkdir -p $new_d
    for f in `ls $d`
    do
        echo "   + Creando " $f
        # se pasa a txt
        $smf2txt -f "%p %o %d %v %c" $d/$f > $new_d/${f}
        # se obtiene el skyline
        $smf2txt -f "%p %o %d %v %c" -p 1 $d/$f > $new_d/${f}.sky
    done
    
done
