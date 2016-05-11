#!/usr/bin/python
#===============================================================================
# Mejorando la eficiencia/velocidad del programa
#===============================================================================
import sys
import os
import re
import random
from pprint import pprint

import lmidi


# ------------------------------------------------------------------------------

# get value from probability density function
def get_pdf(distribution, r=-1):
    acc_prob=[]  # accumulated probability
    keys=[]  # keys for the distribution dictionary
    for i in distribution.keys():
        len_ = len(acc_prob)
        if( len_ > 0):
            acc_prob.append(acc_prob[len_-1] + distribution[i] )
        else:
            acc_prob.append(distribution[i])
        keys.append(i)
    # the selected value for keys is the one that with max 
    # accumulated probability  < t
    if r== -1:
        r = random.random()
    value = keys[0]
    i = 1
    while i<len(keys):
        if r>acc_prob[i-1] and r<=acc_prob[i]:
            value= keys[i]
        i += 1
    return value


# Variables --------------------------------------------------------------------
head="""# path melody.mid
@resolution 240
@format "%p %o %d %v"
@track 1 Melody--BBOK
79 0 60 100
79 120 60 100"""
time = 120
duration = 60
velocity = 100

 

# total de notas en el fichero midi creado
num_notas = 100

# fichero midi de muestra
midi_file="melody.mid"



m=lmidi.Tsmf2txt(midi_file,True)
b = m.bigram_pitch_interval(1)


# Se genera el fichero midi
print head
last_note = 79
last_interval = 0
onset=240

for n in range(num_notas):
    new_interval = get_pdf(b[last_interval])
    new_note = last_note + new_interval
    print "%s %s %s %s" % (new_note, onset, duration, velocity)
    last_interval = new_interval
    last_note = new_note
    onset += time


