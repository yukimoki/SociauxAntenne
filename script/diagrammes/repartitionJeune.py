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

def somme(liste):
    _somme = 0
    for i in liste:
        _somme = _somme + i
    return _somme

def moyenne(liste):
    return somme(liste)/len(liste)
def genData(seuil):
    """
    in: seuil=float,
    out: tableau [distance] 
    """
    data = []
    
    
    for index, row in carres_df.iterrows():
        #bar.next()
        popc= row['poptot']
        jeunes = row['pcjeunes1525']*100
        if (jeunes<seuil and jeunes>=seuil-1):
            for i in range (1,5): # 4 points du carré
                dist = int(row['DistSupProchePt'+str(i)]) # distance de l'antenne au point
                data.append(dist)
    
        
    #bar.finish()
    
    return data

def comptcarre(seuil):
    
    nbcarre=0
    
    for index, row in carres_df.iterrows():
        #bar.next()
        popc= row['poptot']
        jeunes = row['pcjeunes1525']*100
        if (jeunes<seuil):
            if (jeunes>=seuil-1):
                nbcarre+=1
    print(nbcarre)
        
    #bar.finish()
    
    return nbcarre

# Main
start_time = time.time()
df = []
moy=[]
carre=0
#grille
fig = plot.figure()
ax = fig.add_subplot(1, 1, 1)

y_min = 0
y_max = 10000

plot.ylim(y_min,y_max)

grid_y_ticks = np.arange(y_min, y_max, 100)

ax.set_yticks(grid_y_ticks , minor=True)

ax.grid(which='minor', alpha=100, linestyle='--')


for i  in range(1,31):
    df.append(genData(i))
    #carre+=comptcarre(i)
    print(len(df))
    #print(carre)

for i in range(0,30):
    moy.append(somme(df[i]))
moyenne(moy)
print(moy)
plot.boxplot(df)
plot.grid()
plot.xlabel('pourcentage de la population jeune')
plot.ylabel("Distance au support le plus proche (m)")
plot.savefig('repjeune.pdf')
plot.show()


print("Temps d'exécution: %s secondes" % (time.time() - start_time))


# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html