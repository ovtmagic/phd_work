
* Construcción de los ficheros CSV para los conjuntos de validacion.
* Etiquetado (manual) de las pistas de bajo -> Revisión de los ficheros CSV creados.


* Programa: csv.py
./csv.py <train_arff> <corpus dir>
salida (standard output): fichero csf

Ejemplo ./csv.py bass_cla200.arff clasica > clasica.csv


* Programa: csv_melody_tagger.csv
Etiqueta las pistas de melodia de un fichero csv (en este caso se utiliza el
fichero csv con las pistas de bajo ya etiquetadas). El resultado se muestra por
la salida estandard.
Si el nombre de la pista contiene: bbok, la pista se etiqueta como melodia.
En "/tmp/mir/<corpus>" deben estar los ficheros MIDI.

./csv_melody_tagger.py <fichero csv> <corpus>

Ejemplo: ./csv_melody_tagger.py clasica.csv clasica > clasica.melody.csv



Errores:
smf2txt Berlioz_Hector_Absence.mid|grep track
Bad Message Buffer...
 length=0 buffer=144

smf2txt -p 1 Vanessa_Paradis_Marylin_et_John.kar 
Violación de segmento



Dudas:

- Sólo partes de la pista contienen la línea de bajo. El resto, por decirlo de alguna manera, contienen parte instrumenta, pero no es la línea de bajo


Changelog:
2012-07-18	Creacion de csv_melody_tagger.py
