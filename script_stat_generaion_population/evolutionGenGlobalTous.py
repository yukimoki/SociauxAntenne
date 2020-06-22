import csv
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

start_time = time.time()

#represente les tranches de population
tabListPop = [[0, 50], [50, 100], [100, 250], [250, 500], [500, 1000], [1000, 5000], [5000, 10000], [10000, 20000], [20000, 40000], [40000, 60000], [60000, 80000], [100000, 120000], [120000, 140000], [140000, 200000], [200000, 400000], [400000]]
tabAnnee = [[2011], [2011, 2014], [2014, 2017], [2017]]
#correspond à la 4G dans la table EMETTEUR.csv

generation = "LTE"

figsizeNombres = (13, 10)
figsizePourcent = (15, 10)
titre  = "Nombre d'émetteurs 4G par année et par population"
titrePourcentage  = "Pourcentage d'émetteurs 4G par année et par population"
tailleTitre = 25

texteOrdonneeGlobal = "Nombre d'émetteurs"
texteAbscisseGlobal = "Nombre d'habitants en milliers"
texteOrdonneePourcentage = "Pourcentage d'émetteurs"
texteAbscissePourcentage = "Nombre d'habitants en milliers"
tailleOrdonnee = 15
tailleAbscisse = 15

#nb de tranches de populations
nbListPop = len(tabListPop)

setsPopulation  = [set() for i in range(nbListPop)]

nbAnnee = len(tabAnnee)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

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

with open('../script/tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
	file_reader = csv.reader(File, delimiter=';')
	next(file_reader)
	for row in file_reader:

		i = 0

		trouve = False

		habitants = int(row[2])

		while i < nbListPop and trouve==False:

			if i == nbListPop - 1 and habitants>=tabListPop[i][0]:
				trouve = True
				temp = row[0].split(",")
				for j in temp:
					setsPopulation[i].add(j)

			elif(habitants>=tabListPop[i][0] and habitants<tabListPop[i][1]):
				trouve = True
				temp = row[0].split(",")
				for j in temp:
					setsPopulation[i].add(j)
			i += 1

#tableau dont la clé est l'id du support et la valeur la région dans laquelle il se trouve
codePostalSupport = {}

with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:
    	codePostalSupport[support[0]] = support[5]



with open('../script/tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
	file_readerEme = csv.reader(FileEme, delimiter=';')
	next(file_readerEme)

	#tableau 2D qui représente chaque ville le nombre d'antennes 4G par année, Boiron puis Saint-Étienne puis Lyon
	tabAnneePop = [[0 for tranchePop in range(nbListPop)] for annee in range(len(tabAnnee) + 2)]

	for emetteur in file_readerEme:

		idSup = emetteur[1]

		if(idSup in codePostalSupport and generation in emetteur[3]):

			dateMiseEnService = emetteur[4]

			if(dateMiseEnService != ''):

				annee = int(dateMiseEnService[6:])

				indiceAnnee = 0

				i = 0

				trouveIndiceAnnee = False

				while i < nbAnnee and trouveIndiceAnnee==False:

					if(i == 0 and annee < tabAnnee[i][0]):
						trouveIndiceAnnee = True
						indiceAnnee = i
					if(i == nbAnnee-1 and annee > tabAnnee[i][0]):
						trouveIndiceAnnee = True
						indiceAnnee = i
					if(i != 0 and i != nbAnnee-1 and annee >= tabAnnee[i][0] and annee <= tabAnnee[i][1]):
						trouveIndiceAnnee = True
						indiceAnnee = i

					i += 1

				j = 0

				trouveTranchePop = False

				tranchePop = 0

				while j < nbListPop and trouveTranchePop == False:

					if(setsPopulation[j].__contains__(codePostalSupport[idSup].replace("'", ""))):
						trouveTranchePop = True
						tranchePop = j

					j += 1

				if trouveTranchePop and trouveIndiceAnnee:
					tabAnneePop[indiceAnnee][tranchePop] += 1

	columns = ["" for i in range(nbAnnee)]

	for i in range(1, nbAnnee - 1):
		columns[i] = str(tabAnnee[i][0]) +"-"+ str(tabAnnee[i][1])

	columns[0] = "<"+str(tabAnnee[0][0])
	columns[nbAnnee-1] = ">"+str(tabAnnee[nbAnnee-1][0])

	index = ["" for i in range(nbListPop)]

	for i in range(nbListPop-1):
		valMin = tabListPop[i][0]/1000
		valMax = tabListPop[i][1]/1000
		if(is_integer(valMin)):
			index[i] = str(int(valMin)) + "-"
		else:
			index[i] = str(valMin) + "-"
		if(is_integer(valMax)):
			index[i] += str(int(valMax))
		else:
			index[i] += str(valMax) 
    
	if(is_integer(tabListPop[nbListPop-1][0]/1000)):
		index[nbListPop-1] = ">="+str(int(tabListPop[nbListPop-1][0]/1000))
	else:
		index[nbListPop-1] = ">="+str(tabListPop[nbListPop-1][0]/1000)

	plt.rcParams["figure.figsize"] = figsizeNombres

	fig, ax = plt.subplots()

	ax.grid(b=True, which='major', axis='both')

	ind = np.arange(len(tabAnneePop[0]))

	data = {}

	for i in range(nbAnnee):
		data[columns[i]] = tabAnneePop[i]

	maxSize = 0

	for i in range(nbAnnee):
		if max(tabAnneePop[i]) > maxSize:
			maxSize = max(tabAnneePop[i])

	maxSize += maxSize*0.02

	bar_plot(ax, data, total_width=1, single_width=0.9)

	ax.set_ylabel(texteOrdonneeGlobal, fontsize = tailleOrdonnee)
	ax.set_xlabel(texteAbscisseGlobal, fontsize = tailleAbscisse)
	ax.set_title(titre, fontsize = tailleTitre)
	ax.set_xticks(ind)
	ax.set_yticks(np.arange(0, maxSize, 1000.0))
	ax.set_xticklabels(index)

	fig.tight_layout()

	plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/statAnneeGlobal.png')

	plt.clf()

	plt.rcParams["figure.figsize"] = figsizePourcent

	fig, ax = plt.subplots()

	ax.grid(b=True, which='major', axis='both')

	maxNbPop = [0 for i in range(nbListPop)]

	for i in range(nbListPop):
		for j in range(nbAnnee):
			maxNbPop[i] += tabAnneePop[j][i]

	df = pd.DataFrame(data=data)

	for i in range(nbAnnee):
		for j in range(nbListPop):
			df[columns[i]][j] = (df[columns[i]][j]/maxNbPop[j])*100

	dataPourcent = {}

	maxPourcent = 0

	for key in df:
		dataPourcent[key] = df[key]
		if max(dataPourcent[key]) > maxPourcent:
			maxPourcent = max(dataPourcent[key])

	maxPourcent += maxPourcent*0.02

	bar_plot(ax, dataPourcent, total_width=1, single_width=0.9)

	ax.set_ylabel(texteOrdonneePourcentage, fontsize = tailleOrdonnee)
	ax.set_xlabel(texteAbscissePourcentage, fontsize = tailleAbscisse)
	ax.set_title(titrePourcentage, fontsize = tailleTitre)
	ax.set_xticks(ind)
	ax.set_yticks(np.arange(0, maxPourcent, 2.0))
	ax.set_xticklabels(index)

	plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/statAnneeGlobalPourcentage.png')
    
print("Temps d execution total: %s secondes ---" % (time.time() - start_time))