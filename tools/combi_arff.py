#!/usr/bin/python

###############################################################################
#
# combina varios ficheros arff
#
###############################################################################
import sys
import re




def read_header(filename):
    header = ""
    f = open(filename, 'r')
    l = f.readline()
    while l and not re.search("^@data",l):
        header = header + l
        l = f.readline()
    if l:
        header = header + l
    f.close()
    return header
    



def read_data(filename):
    data = ""
    f = open(filename, 'r')
    add_data = False
    l = f.readline()
    while l:
        if add_data and l != "\n":
            data = data + l
        if re.search("^@data",l):
            add_data = True
        l = f.readline()
    return data


arff = ""
for filename in sys.argv[1:]:
    if not arff:
        arff = read_header(filename)
    arff = arff + read_data(filename)
    


print arff