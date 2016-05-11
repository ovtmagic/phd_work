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



dist1={
       'b':0.20,
       'c':0.30,
       'd':0.50}

i=0.0
while i <= 1.0:
    print i , get_pdf(dist1, i)
    i += 0.05