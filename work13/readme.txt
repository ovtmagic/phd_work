Construcción de un segundo clasificador

A partir de los valores P(M|t), p(B|t) y p(A|t) de cada pista
se construye un clasificador para determinar si la pista es
de bajo, melodía o acompañamiento.

Se crea el script get_prob_and_tags2_loo para generar el fichero
de probabilidades para cada base de datos utilizando el schema
leave-one-out (tanto en formato txt como csv) 