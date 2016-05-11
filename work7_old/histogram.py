#!/usr/bin/python


# -*- coding: utf-8 -*-





#Se importa numpy como np


import numpy as np


import matplotlib.pyplot as plt





import scipy.stats as st


#Se importa pylab


from pylab import *





#Generacion de numeros aleatorios menores que 1000


x = np.random.randn(1000)





#Generacion de los datos del histograma con scipy.stats.
n, low_range, binsize, extrapoints = st.histogram(x)
#define el rango superior
upper_range = low_range+binsize*(len(n)-1)





#Se calcula los intervalos discretos


bins = np.linspace(low_range, upper_range, len(n))


#Generacion del grafico de barras


bar(bins, n, width=0.3, color='blue')


#Etiquetas de los ejes X y Y.


xlabel('X', fontsize=15)


ylabel('numero de datos discretos', fontsize=15)


#Se muestra la grafica.

show()
