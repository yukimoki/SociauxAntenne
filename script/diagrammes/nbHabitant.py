import os
import csv
import math
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import time


# Paths
cAll = './CarresDistSupProche.csv'
cStats = './StatsSocioCarres.csv'

# Files
print('Ouverture des fichiers...')
with open(cAll) as carre_file:
    cAll_df = pd.read_csv(carre_file, sep=';', quotechar="'")
    print('\t-Carrés INSEE avec leurs supports')
with open(cStats) as carre_file:
    cStats_df = pd.read_csv(carre_file, sep='\s+')
    print('\t-Statistiques INSEE')
print('Jointure des fichiers...')
carres_df = cAll_df.join(cStats_df.set_index('LAEA'), on='IDcrs')
# Functions
def genData(seuil=0.5):
    """
    in: seuil=float,
    out: nbHabitant = int
    nbHabitant est le nombre d'Habitant du pour un pourcentage de population jeune donne
    """
    
    nbHabitant=0
    nbcarre=0
    for index, row in carres_df.iterrows():
        popc= row['poptot']                 #population du carre
        jeunes = row['pcjeunes1525']*100    #pourcentage de jeune du carre
        if (jeunes<seuil and jeunes>=seuil-1):
            nbHabitant+=popc
            nbcarre+=1    
    
    print(nbcarre)
    return nbHabitant


# Main
start_time = time.time()
df = []


for i  in range(1,31):
    df.append(genData(seuil=i))
    print(len(df))
grph=pd.DataFrame(df, columns=['Population'], dtype=float)
grph.to_csv(r'repatitionPopulationjeune15-25.csv', sep='\t', encoding='utf-16', index=False)
print("Temps d'exécution: %s secondes" % (time.time() - start_time))


# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html