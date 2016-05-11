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

def pdf_diana_old(b, last_interval):
    r = random.random()
    keys = b[last_interval].keys()
    i = 0
    sum_prob = b[last_interval][keys[i]]
    while r >= sum_prob:
        i += 1
        sum_prob += b[last_interval][keys[i]] #keys
    
    new_interval = keys[i]
    return new_interval

def pdf_diana(distribution):
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
    r = random.random()
    #r=0.41
    i = 1
    while i < len(keys) and r > acc_prob[i]:
        i += 1
    value = keys[i]
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
b = m.bigram_pitchtime(1)
pprint(b)

# Se genera el fichero midi
print head
last_note = 79
#last_interval = 0
onset=240
last_time=111

for n in range(num_notas):
    (new_note, time) = pdf_diana(b[(last_note,last_time)])
    print "%s %s %s %s" % (new_note, onset, duration, velocity)
    last_note = new_note
    onset += time
    last_time=time


