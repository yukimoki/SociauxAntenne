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
    """
    in:liste = tableau[float]
    out:_somme = float
    _somme est la somme des éléments du tableau liste
    """
    _somme = 0
    for i in liste:
        _somme = _somme + i
    return _somme

def moyenne(liste):
    """
    in:liste = tableau[float]
    out: la moyenne du tableau liste
    """
    return somme(liste)/len(liste)

def genData(seuil):
    """
    in: seuil=float,
    out: data = tableau [float] 
    cette fonction retourne la liste des distances aux supports les plus proche pour un pourcentage de jeune dans un carre 
    """
    data = []
    
    
    for index, row in carres_df.iterrows():
        popc= row['poptot'] # population du carre
        jeunes = row['pcjeunes1525']*100    #pourcentage de jeune dans le carre
        if (jeunes<seuil and jeunes>=seuil-1):
            for i in range (1,5): # 4 points du carré
                dist = int(row['DistSupProchePt'+str(i)]) # distance de l'antenne au point
                data.append(dist)

    
    return data

def comptcarre(seuil):
    """
    in: seuil = float,
    out: nbcarre = int
    nbcarre et le nombre de carre correspondant au pourcentage de jeune indiquer par seuil 
    """
    nbcarre=0
    
    for index, row in carres_df.iterrows():
        jeunes = row['pcjeunes1525']*100    #pourcentage de jeune dans le carre
        if (jeunes<seuil):
            if (jeunes>=seuil-1):
                nbcarre+=1
    print(nbcarre)
    
    return nbcarre

# Main
start_time = time.time()
df = []
moy=[]
carre=0
#grille
fig = plot.figure()
ax = fig.add_subplot(1, 1, 1)

y_min = 0   #indique la valeur la plus basse de la figure generee
y_max = 2000    #indique la valeur la plus haute de la figure generee

plot.ylim(y_min,y_max)

grid_y_ticks = np.arange(y_min, y_max, 100) #permet d'afficher une grille

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
plot.boxplot(df)    #cree uns boite à moustache 
plot.grid()
plot.xlabel('pourcentage de la population jeune')
plot.ylabel("Distance au support le plus proche (m)")
plot.savefig('repjeuneZoom.pdf') #sauvegarde la figure avec le nom mit en parametre
plot.show()


print("Temps d'exécution: %s secondes" % (time.time() - start_time))


# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html