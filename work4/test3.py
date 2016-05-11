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
head="""# path Michael_Jackson_Billie_Jean_1.kar
@resolution 192
@format "%p %o %d %v"
@track 1 Soft Karaoke
@track 2 Words
@track 3 Melody--BBOK
73 11712 31 109
73 11808 28 123"""

time = 96
duration = 60
velocity = 100

# total de notas en el fichero midi creado
num_notas = 1000

# fichero midi de muestra
midi_file="melody.mid"
midi_file="/tmp/mir/test/Michael_Jackson_Billie_Jean_1.kar"
track_num=5



m=lmidi.Tsmf2txt(midi_file,True)
b = m.bigram_pitchtime(track_num)
#pprint(b)


# Se genera el fichero midi
print head
last_note = 30
last_time = 96
#last_interval = 0
onset=96*2

for n in range(num_notas):
    (new_note,new_time) = get_pdf(b[(last_note,last_time)])
    print "%s %s %s %s" % (new_note, onset, duration, velocity)
    last_note = new_note
    last_time = new_time
    onset += new_time


