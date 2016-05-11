#!/usr/bin/python
import sys
import os
import lmidi
from pprint import pprint


midi_file = "/tmp/mir/kar/ZZ_Top_Gimme_all_your_lovin.kar"


x = lmidi.Midi()
x.load_midi(midi_file)
x.load_skyline(midi_file)
x.gen_descriptors()

print "tracks:"
print x.tracks.keys() 

print x.get_arff_header('test')
print x.get_arff([4])
