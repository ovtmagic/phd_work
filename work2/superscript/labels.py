#!/usr/bin/python
import sys
import re
import os


file="kar.csv"






# leemos el fichero --------------------------
file_lines=[]
f=open(file)
for l in f.readlines():
    file_lines.append(l.replace("\r\n","").replace("\n",""))
f.close()

# Main -------------------------------------------

salir=False
i=1
while not salir and i < len(file_lines):
    line = file_lines[i]
    # Se comprueba que aun no se ha revisado
    if not re.search(',"OK',line) and not re.search(',OK',line) and not re.search("Revisar",line) and not re.search("REVISAR",line):
        line_temp=line.split(',')
        print "\n\n\n\n\n\nFile: "+line_temp[0].replace('"','')+".mid"
        print line
        c=os.popen("smf2txt kar/%s.mid |grep track" % line_temp[0])
        print c.read()
        c.close()
        # se lee la pista de bajo
        print "Bass track:"
        b=sys.stdin.readline()[:-1]
        print ">>>>>%s<" % (b)
        new_line=line
        if( b == ""):
            new_line=line+'"OK"'
        elif (b == 'r'):
            new_line = line + ',"REVISAR"'
        elif (b == 'X'):
            salir=True
        else:
            temp=line.split(',')
            temp[3]=b
            new_line=temp[0]
            for j in temp[1:]:
                new_line=new_line+","+j
            new_line=new_line+'"OK-M"'
        #print file_lines[i]
        file_lines[i]=new_line
        print file_lines[i]
        
        

    i=i+1


# Guardamos el fichero ------------------
f=open(file+".new.csv","w")
for l in file_lines:
    #f.write(l+"\r\n")
    f.write(l+"\n")
f.close()


