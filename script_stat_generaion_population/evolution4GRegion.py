import csv
import pandas as pd
import matplotlib.pyplot as plot
import time
import numpy as np

start_time = time.time()

cpSaintEtienne = [42000, 42100, 42230]
cpLyon = [69001, 69002, 69003, 69004, 69005, 69006, 69007, 69008, 69009]
Boiron = 80430

tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

nbTranches = len(tabAnnee) + 1

supportRegions = {}

def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')

#on récupère tous les supports des régions concernées
with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:

    	if(int(support[5]) in cpLyon or int(support[5]) in cpSaintEtienne or int(support[5])==Boiron):
    		supportRegions[support[0]] = support[5]

with open('../tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    #tableau 2D qui représente chaque ville le nombre d'antennes 4G par année, Boiron puis Saint-Étienne puis Lyon
    tabVille = [[0 for annee in range(nbTranches)] for ville in range(3)]

    for emetteur in file_readerEme:

        if(emetteur[1] in supportRegions and "LTE" in emetteur[3]):

            region = int(supportRegions[emetteur[1]])

            dateMiseEnService = emetteur[4]

            if(dateMiseEnService != ''):

	            annee = int(dateMiseEnService[6:])

	            tranche = 0

	            i = len(tabAnnee) - 1

	            trouve = False

	            while i > 0 and trouve==False:

	            	if(annee > tabAnnee[i]):
	            		trouve = True
	            		tranche = i + 1

	            	i -= 1

	            if trouve == False:
	            	if annee > tabAnnee[0] :
	            		tranche = 1
	            	else:
	            		tranche = 0

	            if(region == Boiron):
	            	tabVille[0][tranche] += 1
	            elif (region in cpSaintEtienne):
	            	tabVille[1][tranche] += 1
	            else :
	            	tabVille[2][tranche] += 1


    data = {
        "Boiron":tabVille[0],
        "Saint-Étienne":tabVille[1],
        "Lyon":tabVille[2]
        };

    index = ["" for i in range(nbTranches)]

    for i in range(1, len(tabAnnee)):
    	index[i] = str(tabAnnee[i-1])[2:] +"-"+str(tabAnnee[i])[2:]

    index[0] = "<"+str(tabAnnee[0])
    index[nbTranches-1] = ">"+str(tabAnnee[len(tabAnnee)-1])[2:]

    fig, ax = plot.subplots()

    width = 0.25

    ind = np.arange(len(tabVille[0]))

    barsBoiron = ax.bar(ind + width, tabVille[0], width, label='Inval-Boiron')
    barsSaintEtienne = ax.bar(ind, tabVille[1], width, label='Saint-Étienne')
    barsLyon = ax.bar(ind - width, tabVille[2], width, label='Lyon')
    ax.set_ylabel("Nombre d'émetteurs 4G")
    ax.set_xlabel("Année")
    ax.set_title("Nombre d'émetteurs 4G par année")
    ax.set_xticks(ind)
    ax.set_xticklabels(index)
    ax.legend()

    autolabel(barsBoiron)
    autolabel(barsSaintEtienne)
    autolabel(barsLyon)

    fig.tight_layout()

    plot.savefig('../statistiques/emetteur_population_support/statLyonBoironSaintEtienne.png')
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))