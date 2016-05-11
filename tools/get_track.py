#!/usr/bin/python
import lmidi




filename="/tmp/x/You_Win_Again.MID"
skyline=False

m=lmidi.Tsmf2txt(filename, skyline )
txt=lmidi.Ttxt2smf(m)

txt.set_name("/tmp/x/track1")
#txt.resolution=240
txt.create_midi([1,3,4,5,6,7], skyline) 