#!/usr/bin/python
import sys
import lmidi


def print_header(track_type):
    print """@relation %s

@attribute pm numeric
@attribute pb numeric
@attribute pa numeric
@ATTRIBUTE class { yes no }

@data""" % track_type


#--------------------------------------------------------------------------------
if (len(sys.argv) == 3) :
    track_type = sys.argv[1]
    csv_filename = sys.argv[2]
else:
    print """ ./new_arff.py <bass|melody|accomp> <csv_file>
        <bass|melody|accomp>: track_type
        <csv_file>: fichero csv con las probabilidades de melodia,bajo,accomp
    """
    sys.exit(1)


print_header(track_type)

# read csv file and print arff lines
f = open(csv_filename)
for l in f.readlines()[1:]:
    #print l 
    pm = l.split(',')[2]
    pb = l.split(',')[3]
    pa = l.split(',')[4]
    tag = l.split(',')[6]
    if tag == track_type:
        class_ok = 'yes'
    else:
        class_ok = 'no'
    print "%s,%s,%s,%s" % (pm, pb, pa, class_ok)
    
    
f.close()