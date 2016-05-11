#!/usr/bin/python
#===============================================================================
# Combina dos ficheros csv. 
#
# ./combi_csv.py <src file> <dst file> <src column> <dst column>
# Muestra el resultado por salida estandar.
# El resultado es el fichero <dst file> pero cambiando la coluna <dst> por la
# columna <src> del fichero <src file>.
# La primera columnta es la 0 [col 0; col 1; col 2;...]
#===============================================================================
import sys

#print sys.argv, len(sys.argv)


# caracter separador
_sep=','

# Se leen los argumentos
if len(sys.argv) == 5:
    file_src = sys.argv[1]
    file_dst = sys.argv[2]
    col_src = int(sys.argv[3])
    col_dst = int(sys.argv[4])
elif len(sys.argv) == 3:
    file_src = sys.argv[1]
    file_dst = sys.argv[2]
    col_src = -1
    col_dst = -1
else:
    print "Error:  ./combi_csv.py <src file> <dst file> <src column> <dst column>"
    sys.exit()
    
#print file_src, file_dst, col_src, col_dst
# se leen los ficheros
dic_src = {}
dic_dst = {}
# fichero origne
f = open(file_src)
file_lines = f.read().split('\n')
first_line=file_lines[0]
for l in file_lines[1:]:
    l_split=l.split(_sep)
    _filename = l_split[0]
    if _filename:
        dic_src[_filename] = l_split[1:]
f.close()    

# fichero destino
g = open(file_dst)
file_lines = g.read().split('\n')
for l in file_lines[1:]:
    l_split=l.split(_sep)
    _filename = l_split[0]
    if _filename:
        dic_dst[_filename] = l_split[1:]
        #-------------------------------------------------------------------
        # Se combina el fichero origen con el fichero destino
        #-------------------------------------------------------------------
        if col_src == -1: # se anaden todas las columnas de src a dst
            if _filename in dic_src.keys():
                dic_dst[_filename] = dic_dst[_filename] + dic_src[_filename]
        elif col_dst >= len( dic_dst[_filename]): # se pone al final de la linea
            if _filename in dic_src.keys():
                dic_dst[_filename].append(dic_src[_filename][col_src-1])
            else:
                dic_dst[_filename].append('') 
        else: # se sustituye la comumna dst por la src
            if _filename in dic_src.keys():
                
                #print " - d ", dic_dst[_filename]
                #print " - o ", dic_src[_filename]
                dic_dst[_filename][col_dst-1] = dic_src[_filename][col_src-1]
            else:
                dic_dst[_filename][col_dst] = ''
g.close()


# Se imprime el resultado
print first_line
for _filename in sorted(dic_dst.keys(), key=str.lower):
    line = _filename
    for i in dic_dst[_filename]:
        line = line +"," +i
    print line