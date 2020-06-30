# -*-coding:UTF-8 -*
import csv
import pandas as pd
import sys
from progress.bar import Bar
import matplotlib.pyplot as plt
import stat
import time
import numpy as np

start_time = time.time()

figsize = (13, 10)

# Initialisation des dataframes
df_carres_sup = pd.read_csv('tables/finalDB/CarresDistSupProche.csv', delimiter=";", usecols=["IDcrs", "IdSupProchePt1", "DistSupProchePt1", "IdSupProchePt2", "DistSupProchePt2", "IdSupProchePt3", "DistSupProchePt3", "IdSupProchePt4", "DistSupProchePt4"])
df_carres_socio = pd.read_csv('tables/finalDB/StatsSocioCarres.csv', delimiter="\t", usecols=["LAEA", "poptot", "pcmenagespauvres"])

# Jointure des df carres dist et socio
df_carres = df_carres_sup.join(df_carres_socio.set_index('LAEA'), on='IDcrs')

df_carres = df_carres.loc[df_carres['poptot'] > 100]


maxPoptotal = 0
maxPopPauvre = 0

# Traitement
dict_square = dict()  # {id carre: [dist_min_to_support, pop_total_carre, pop_pauvre_carre]}
bar = Bar('find total nbHab for each holder', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=len(df_carres)-1)

for idx, carre in df_carres[
	["DistSupProchePt1", "DistSupProchePt2", "DistSupProchePt3", "DistSupProchePt4"]].iterrows():
	id_carre, pop_total, pc_pauvre = df_carres.loc[idx, ['IDcrs', 'poptot', 'pcmenagespauvres']].values

	pop_pauvre = pop_total * pc_pauvre

	min_dist = 99999
	for dist_sup in carre:
		if dist_sup < min_dist:
			min_dist = dist_sup

	dict_square[id_carre] = [min_dist, pop_total, pop_pauvre]
	bar.next()
bar.finish()

df = pd.DataFrame.from_dict(data=dict_square, columns=['DIST_MIN_SUP', 'POP_TOTAL', 'POP_PAUVRE'], orient='index')

intervalles = [[100,150], [150,200], [200,250], [250,300], [300,350],[350,400] ,[400,450], [450,500], [500,750], [750,1000], [1000,1500], [1500,2000],[2000,2500] ,[2500,3000], [3000,3500], [3500,4384]]
nbIntervalles = len(intervalles)

#tableau de tableau
#tabPop[0] = pop_total
#tabPop[1] = pop_pauvre
#tabPop[2] = nbCarre
#tabPop[0][0] = distMoy du 1 er intervalle
tabPop = [[0 for i in range(nbIntervalles)] for i in range(3)]
popEtudie = ["POP_TOTAL","POP_PAUVRE"]

for i in range(2):
	for j in range(nbIntervalles):
		serie_interval = df[(df[popEtudie[i]] >= intervalles[j][0]) & (df[popEtudie[i]] < intervalles[j][1])]
		moy_dist_interval = serie_interval['DIST_MIN_SUP'].mean()
		tabPop[i][j] = moy_dist_interval
		if(i==0):
			tabPop[2][j] = serie_interval.count()

index = ["" for i in range(nbIntervalles)]

print(tabPop[0])
print(tabPop[1])

for i in range(nbIntervalles):
	index[i] = str(intervalles[i][0]) + "-" + str(intervalles[i][1])

dataIntervalles = {}

for i in range(len(popEtudie)):
	dataIntervalles[popEtudie[i]] = tabPop[i]

for i in range(nbIntervalles):
	print(tabPop[2][i])

def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())

df = pd.DataFrame(data = dataIntervalles)

plt.rcParams["figure.figsize"] = figsize
fig, ax = plt.subplots()
ind = np.arange(len(tabPop[0]))
bar_plot(ax, dataIntervalles, total_width=1, single_width=0.9)
ax.set_xticks(ind)
ax.set_xticklabels(index)

plt.ylabel("Distance en mètres")
plt.xlabel("Intervalles de population en habitants")
plt.grid(b=True, which='major', axis='both')

plt.show()

plt.savefig("tables/test2.png")

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))
