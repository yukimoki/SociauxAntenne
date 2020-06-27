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

def rep():
    """
    in: seuil=float,
    out: tableau [distance] 
    """
    data = []
    nbcarre=0
    
    for index, row in carres_df.iterrows():
        #bar.next()
        popc= row['poptot']
        for i in range (1,5): # 4 points du carré
            dist = int(row['DistSupProchePt'+str(i)]) # distance de l'antenne au point
            data.append(dist)
        nbcarre+=1
        
    #bar.finish()
    print(nbcarre)
    return data


# Main
start_time = time.time()
df = []
fig = plot.figure()
ax = fig.add_subplot(1, 1, 1)

y_min = 0
y_max = 10000

plot.ylim(y_min,y_max)

grid_y_ticks = np.arange(y_min, y_max, 100)

ax.set_yticks(grid_y_ticks , minor=True)

ax.grid(which='minor', alpha=100, linestyle='--')

df.append(rep())
print(len(df))
plot.boxplot(df)
plot.grid(which='both')
plot.ylabel("Distance au support le plus proche (m)")
plot.savefig('reppop.pdf')
plot.show()

print("Temps d'exécution: %s secondes" % (time.time() - start_time))


# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html