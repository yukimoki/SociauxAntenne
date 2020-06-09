import os
import csv
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import time
from progress.bar import IncrementalBar

# Paths
cAll = 'data/CarresDistSupProche.csv'
cStats = 'data/carres-stats-avec-nb-antennes'

# Files
print('Ouverture des fichiers...')
with open(cAll) as carre_file:
    cAll_df = pd.read_csv(carre_file, sep=';', quotechar="'")
    print('\t-Carrés INSEE avec leurs supports')
with open(cStats) as carre_file:
    cStats_df = pd.read_csv(carre_file, sep='\s+')
    print('\t-Statistiques INSEE')

# Functions
def plot_chart(detail=10, stat='poptot', threshold=0, tech='ALL', max_search_dist=17000):
    """
    in: detail=échantillon (nombre de barres), 
        stat=statistique INSEE à évaluer, 
        threshold=valeur de stat min pour être retenue (si négative, max), 
        tech=technologie de l'antenne
        max_search_dist=distance de recherche en km
    out: tableau [distance, population] associé
    """
    def _verify_tech (_row):
        if (tech!='ALL'):
            emetteur = cEmetteur_df[cEmetteur_df['ID_SUP']==int(_row['SupProchePt'+str(i)].split('-')[0])]
            for description in emetteur.values:
                if tech in description[3]:
                    return True
            return False
        return True

    data = []
    interval = max_search_dist/detail # 17km = distance max au support possible
    msd = round((detail*interval)/1000, 2)
    negative_threshold = (threshold<0)
    if (negative_threshold):
        threshold*=-1
    for i in range (detail):
        data.append([str(round((i*interval)/1000, 2))+' à '+str(round(((i+1)*interval-1)/1000, 2)), 0])
    print('Jointure des fichiers...')
    carres_df = cAll_df.join(cStats_df.set_index('LAEA'), on='IDcrs')
    bar = IncrementalBar('Génération des données', max=len(cAll_df))
    for index, row in carres_df.iterrows():
        bar.next()
        if (_verify_tech(row)):
            for i in range (1,4): # 4 points du carré
                dist = int(row['DistSupProchePt'+str(i)]) # distance de l'antenne au point      
                pop = row['poptot'] / 4
                statpc = row[stat]
                if ((statpc>=threshold and not negative_threshold) or (statpc<=threshold and negative_threshold)):
                    if (dist//interval < len(data)):
                        data[round(dist//interval)][1]+=pop
                    else:
                        if (data[-1][0] == 'Plus de '+str(msd)):
                            data[-1][1]+=pop
                        else:
                            data.append(['Plus de '+str(msd), 0])

    bar.finish()
    df = pd.DataFrame(data, columns=['Distance (km)','Population'], dtype=float)
    print(df)
    df.to_csv(r'statpop250m.csv', sep='\t', encoding='utf-16')
    df.plot.bar(x="Distance (km)", y="Population", rot=25, title="Distances des supports les plus proches aux carrés de population")
    plot.xlabel("Distance au support le plus proche (km)")
    plot.ylabel("Volume total de population")

# Main

start_time = time.time()
plot_chart(detail=25, stat='poptot', threshold=0, tech='ALL', max_search_dist=10000)
#plot.savefig('statpop.pdf')
print("Temps d'exécution: %s secondes" % (time.time() - start_time))
plot.show()

# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html