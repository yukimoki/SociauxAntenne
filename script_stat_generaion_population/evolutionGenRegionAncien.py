import csv
import pandas as pd
import matplotlib.pyplot as plot
import time
import numpy as np
from datetime import datetime

start_time = time.time()

#correspond à la 4G dans la table EMETTEUR.csv
generation = "LTE"

figsize = (12, 10)
titre  = "Pourcentage d'émetteurs mise en service par ville et année"
tailleTitre = 25

axeOrdonnee = "Pourcentage d'émetteurs"
axeAbscisse = "Année"
tailleOrdonnee = 15
tailleAbscisse = 15

regions = [[69001, 69002, 69003, 69004, 69005, 69006, 69007, 69008, 69009], [42000, 42100, 42230], [80430]]
nomRegions = ["Lyon", "Saint-Étienne", "Inval-Boiron"]
linestyles = ["-", "--", "-."]
markers = ["o", "o", "o"]

nbRegions = len(regions)

tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

nbTranches = len(tabAnnee) + 1

supportRegions = {}

premierEmetteurParSupport = {}

#on récupère tous les supports des régions concernées
with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:

        for i in range(nbRegions):
            if(int(support[5]) in regions[i]):
                supportRegions[support[0]] = support[5]

#on récupère pour chaque support l'émetteur 4G le plus ancien
with open('../tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    for emetteur in file_readerEme:

        idSup = emetteur[1]

        if(idSup in supportRegions and generation in emetteur[3]):

            dateMiseEnService = emetteur[4]

            if(dateMiseEnService != ''):

                annee = int(dateMiseEnService[6:])

                if(idSup in premierEmetteurParSupport):
                    oldAnnee = int(premierEmetteurParSupport[idSup])

                    if oldAnnee > annee:
                        premierEmetteurParSupport[idSup] = dateMiseEnService[6:]
                else:
                    premierEmetteurParSupport[idSup] = dateMiseEnService[6:]

    
#tableau 2D qui représente chaque ville le nombre d'antennes 4G par année pour chaque region
tabVille = [[0 for annee in range(nbTranches)] for ville in range(nbRegions)]

for key in premierEmetteurParSupport:

    idSup = key

    region = int(supportRegions[idSup])

    annee = int(premierEmetteurParSupport[idSup])

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

    for j in range(nbRegions):
        if region in regions[j]:
            tabVille[j][tranche] += 1


index = ["" for i in range(nbTranches)]

for i in range(1, len(tabAnnee)):
    index[i] = str(tabAnnee[i-1]) +"-"+str(tabAnnee[i])

index[0] = "<"+str(tabAnnee[0])
index[nbTranches-1] = ">"+str(tabAnnee[len(tabAnnee)-1])

data = {}

for i in range(nbRegions):
    data[nomRegions[i]] = tabVille[i]

df = pd.DataFrame(data=data)

plot.rcParams["figure.figsize"] = figsize

for i in range(nbRegions):
    df[nomRegions[i]] = df[nomRegions[i]].cumsum()
    nbEmetRegions = [df[nomRegions[j]][len(df[nomRegions[j]]) - 1] for j in range(nbRegions)]
    df[nomRegions[i]] = (df[nomRegions[i]]/nbEmetRegions[i])*100
    plot.plot(index, df[nomRegions[i]], label = nomRegions[i] + ": " + str(nbEmetRegions[i]), marker = markers[i], linestyle = linestyles[i])


plot.grid(b=True, which='major', axis='both')
plot.title(titre, fontsize=tailleTitre)
plot.ylabel(axeOrdonnee, fontsize=tailleOrdonnee)
plot.xlabel(axeAbscisse, fontsize=tailleAbscisse)
plot.yticks(np.arange(0, 101, 5.0))

plot.legend()

plot.savefig('../statistiques/emetteur_population_support/StatParAnnee/statRegionsEmetAncien.png')
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))