#!/bin/bash

dataset="class_900_6"


mkdir to_remove

# eliminamos los ficheros midi no validos
for i in `grep xxxxx ${dataset}_con_notas.csv |cut -d ";" -f 1`
do
    mv $dataset/$i to_remove
done


# generamos el fichero csv bueno
grep -v xxxxx class_900_6_con_notas.csv |sed "s/\;/\,/g" > ${dataset}.csv
