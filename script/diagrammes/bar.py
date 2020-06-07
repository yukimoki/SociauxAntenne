import csv
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import math
import time
from progress.bar import IncrementalBar

#Path
cAll = 'data/carresALL[essai]avecSup.csv'
cStats = 'data/carres-stats-avec-nb-antennes'
cEmetteur = 'data/EMETTEUR.csv'

#File read
with open(cAll) as carre_file:
    cAll_df = pd.read_csv(carre_file, sep=';', quotechar="'")
with open(cStats) as carre_file:
    cStats_df = pd.read_csv(carre_file, sep='\s+')
    header = list(cStats_df.columns.values)
with open(cEmetteur) as emetteur_file:
    cEmetteur_df = pd.read_csv(emetteur_file, sep=';', quotechar="'")

#Function
def plot_chart(detail=10, stat='poptot', threshold=0, type='LTE'):
    """
    in: detail=échantillon (nombre de barres), stat=statistique INSEE à évaluer, threshold=valeur de stat minimum pour être retenue (si négative, maximum), type=technologie de l'antenne
    out: graphique panda associé
    """
    bar = IncrementalBar('Génération du diagramme', max=len(cAll_df))
    data = []
    stat_index = header.index(stat)
    interval = 17000/detail # 17km = max search dist
    
    for i in range (detail):
        data.append([str(math.floor(i*interval))+' à '+str(math.floor((i+1)*interval-1)), 0])
    for index, row in cAll_df.iterrows():
        bar.next()
        carre = cStats_df[cStats_df['LAEA']==row['IDcrs']]
        for i in range (1,4): # 4 points du carré
            dist = int(row['SupProchePt'+str(i)].split('-')[1]) # distance de l'antenne au point
            pop = carre.values[0][2] / 4 #values[0][2] => poptot
            if (carre.values[0][stat_index] >= threshold):
                data[math.floor(dist//interval)][1]+=pop
    bar.finish()
    df = pd.DataFrame(data, columns=['pop','support'], dtype=float)
    print(df)
    df.plot.bar(x="pop", y="support", rot=25, title="Distances des supports les plus proches aux carrés de population")

#Main
start_time = time.time()
plot_chart(detail=11)
print("Temps d'exécution: %s secondes" % (time.time() - start_time))
plot.savefig('statpop.png')
plot.show()

# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html
