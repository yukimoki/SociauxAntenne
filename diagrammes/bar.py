import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
cAll = 'carresALL[essai]avecSup.csv'
cStats = 'carres-stats-avec-nb-antennes'
with open(cAll) as carre_file:
    cAll = pd.read_csv(carre_file, sep=';', quotechar="'")
with open(cStats) as carre_file:
    cStats = pd.read_csv(carre_file, sep='\s+')

def plot_chart():
    data = []
    for index, row in cAll.iterrows():
        print(index)
        for i in range (1,4): #4 points du carré
            array = []
            array.append(int(row['SupProchePt'+str(1)].split('-')[1])) #distance de l'antenne au point
            array.append(cStats.loc[cStats['LAEA']==row['IDcrs']].values[0][2]) #values[0][2] => poptot
            data.append(array)
    return data

data = plot_chart()
print(data)
df = pd.DataFrame(data,columns=['dist','pop'],dtype=float)
df.plot.hist(x='dist', y='pop', bins=20)
plot.show()
"""
distribution: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.hist.html
"""