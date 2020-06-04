import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import math
import time
from progress.bar import IncrementalBar

cAll = 'carresALL[essai]avecSup.csv'
cStats = 'carres-stats-avec-nb-antennes'
with open(cAll) as carre_file:
    cAll = pd.read_csv(carre_file, sep=';', quotechar="'")
    bar = IncrementalBar('Countdown', max = len(cAll))
with open(cStats) as carre_file:
    cStats = pd.read_csv(carre_file, sep='\s+')
    header = list(cStats.columns.values)

def plot_chart(detail=10, stat='poptot', type='LTE'):
    """
    in: detail=nombre de barres, stat=statistique INSEE à évaluer, type=technologie de l'antenne
    out: graphique panda associé
    """
    data = []
    stat_index = header.index(stat)
    interval = 17000/detail # 17km = max search dist
    
    for i in range (detail):
        data.append([str(math.floor(i*interval))+' à '+str(math.floor((i+1)*interval-1)), 0])
    print(data)
    for index, row in cAll.iterrows():
        bar.next()
        for i in range (1,4): # 4 points du carré
            dist = int(row['SupProchePt'+str(1)].split('-')[1]) # distance de l'antenne au point
            pop = cStats.loc[cStats['LAEA']==row['IDcrs']].values[0][stat_index] / 4 #values[0][2] => poptot
            data[math.floor(dist//interval)][1]+=pop
    bar.finish()
    df = pd.DataFrame(data,columns=['pop','support'],dtype=float)
    print(df)
    df.plot.bar(x="pop", y="support", rot=25, title="Distances des supports les plus proches aux carrés de population")
    plot.show()

plot_chart()

plot.savefig('statpop.png')

# distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html
