2012-10-07

El objetivo es obtener una nueva base de datos de jazz y mœsica cl‡sica
con las pistas de bajo y melod’a etiquetadas.


* crea_csv.py: Modificaci—n del fichero de workx. Crea el fichero csv con la
pista de bajo etiquetada.

* dataset_jazz: obtenida de la p‡gina 'http://www.thejazzpage.de/index1.html'

* b_jazz200.arff. Usada por crea_csv.py para entrenar el algoritmo de 
clasificaci—n de la pista de bajo.

* lmidi.py: Libreria midi

*viewer.py: Utiliza metamidi para sacar alguna informaci—n de los ficheros
midi de un directorio.

* busca_duplicados.py: busca ficheros midi duplicado en todos los directorios
que se le pasan como par‡metros. Busca duplicados exactos, y lo que hace es
comprobar si el hash md5 de dos ficheros son iguales
