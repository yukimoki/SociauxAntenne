import csv
import pandas as pd
import matplotlib.pyplot as plot
import time
import numpy as np

start_time = time.time()

#represente les tranches de population, la premier est entre 0 et tabListPop[0], puis tabListPop[0] et tabListPop[1] etc
tabListPop = [500, 1000, 5000, 10000, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 200000, 400000]

#nb de tranches de populations
nbListPop = len(tabListPop) + 1

setsPopulation  = [set() for i in range(nbListPop)]

tabAnnee = [2011, 2014, 2017]

nbTranches = len(tabAnnee) + 1

with open('../tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
    file_reader = csv.reader(File, delimiter=';')
    next(file_reader)
    for row in file_reader:

        i = nbListPop - 2

        trouve = False

        while i > 0 and trouve==False:

            if(int(row[2])>=tabListPop[i]):
                trouve = True
                temp = row[0].split(",")
                for j in temp:
                    setsPopulation[i].add(j)

            i-=1

        if trouve==False:
            temp = row[0].split(",")
            for j in temp:
                setsPopulation[0].add(j)

d = {}

with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:
    	d[support[0]] = support[5]



with open('../tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
	file_readerEme = csv.reader(FileEme, delimiter=';')
	next(file_readerEme)

	#tableau 2D qui représente chaque ville le nombre d'antennes 4G par année, Boiron puis Saint-Étienne puis Lyon
	tabAnneePop = [[0 for tranchePop in range(nbListPop)] for annee in range(len(tabAnnee) + 2)]

	for emetteur in file_readerEme:

		if(emetteur[1] in d and "LTE" in emetteur[3]):

			dateMiseEnService = emetteur[4]

			if(dateMiseEnService != ''):

				annee = int(dateMiseEnService[6:])

				trancheAnnee = 0

				i = len(tabAnnee) - 1

				trouveTrancheAnnee = False

				while i > 0 and trouveTrancheAnnee==False:

					if(annee > tabAnnee[i]):
						trouveTrancheAnnee = True
						trancheAnnee = i + 1

					i -= 1

				if trouveTrancheAnnee == False:
					if annee > tabAnnee[0] :
						trancheAnnee = 1
					else:
						trancheAnnee = 0

				j = 0

				trouveTranchePop = False

				tranchePop = 0

				while j < nbListPop - 1 and trouveTranchePop == False:

					if(setsPopulation[j].__contains__(d[emetteur[1]].replace("'", ""))):
						trouveTranchePop = True
						tranchePop = j

					j += 1

				if trouveTranchePop == False:
					tranchePop = nbListPop - 1

				tabAnneePop[trancheAnnee][tranchePop] += 1

	columns = ["" for i in range(nbTranches)]

	for i in range(1, len(tabAnnee)):
		columns[i] = str(tabAnnee[i-1])[2:] +"-"+str(tabAnnee[i])[2:]

	columns[0] = "<"+str(tabAnnee[0])
	columns[nbTranches-1] = ">"+str(tabAnnee[len(tabAnnee)-1])[2:]

	index = ["" for i in range(nbListPop)]

	for i in range(nbListPop-1):
		if(tabListPop[i]<1000):
			index[i] = str(tabListPop[i]/1000)
		else:
			index[i] = str(int(tabListPop[i]/1000))
    
	index[nbListPop-1] = ">="+str(int(tabListPop[nbListPop-2]/1000))

	plot.rcParams["figure.figsize"] = (12, 8)

	fig, ax = plot.subplots()

	width = 1/4

	ind = np.arange(len(tabAnneePop[0]))

	ax.bar(ind - width, tabAnneePop[0], width, label='<2011')
	ax.bar(ind, tabAnneePop[1], width, label='2011-2014')
	ax.bar(ind + width, tabAnneePop[2], width, label='2014-2017')
	ax.bar(ind + 2*width, tabAnneePop[3], width, label='>2017')


	ax.set_ylabel("Nombre d'émetteurs 4G")
	ax.set_xlabel("Année")
	ax.set_title("Nombre d'émetteurs 4G par année et par population")
	ax.set_xticks(ind)
	ax.set_xticklabels(index)
	ax.legend()

	fig.tight_layout()

	"""

	plot.grid(b=True, which='major', axis='both')

	plot.plot(index, tabAnneePop[0], label='<2011', marker ="o")
	plot.plot(index, tabAnneePop[1], label='2011-2014', ls = "-.", marker ="o")
	plot.plot(index, tabAnneePop[2], label='2014-2017', ls="--", marker ="o")
	plot.plot(index, tabAnneePop[3], label='>2017', ls= ':', marker ="o")
	plot.title("Nombre d'émetteurs 4G par année et par population", fontsize=25)
	plot.ylabel("Nombre d'émetteurs 4G", fontsize=15)
	plot.xlabel("Année", fontsize=15)

	plot.legend()

	"""

	plot.savefig('../statistiques/emetteur_population_support/StatParAnnee/statAnneeGlobal.png')
    
print("Temps d execution total: %s secondes ---" % (time.time() - start_time))