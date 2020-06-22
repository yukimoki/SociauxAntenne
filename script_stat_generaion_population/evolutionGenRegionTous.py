import csv
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

start_time = time.time()

#correspond à la 4G dans la table EMETTEUR.csv
generation = "LTE"

figsize = (12, 10)
titre  = "Pourcentage d'émetteurs mise en service par region et année"
tailleTitre = 25

axeOrdonnee = "Pourcentage d'émetteurs"
axeAbscisse = "Année"
tailleOrdonnee = 15
tailleAbscisse = 15

tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

regions = [[97200,97234,97212], [12120,12410], [12340,12500,12190], [24620,24260]]
nomRegions = ["Fort-de-France", "Arvieu", "Bozouls", "Les Eyzies"]
linestyles = ["-", "--", "-.", "--"]
markers = ["o", "o", "o","p"]

texteSauvegarde = "statRegionsFABL.png"

nbRegions = len(regions)

nbTranches = len(tabAnnee) + 1

supportRegions = {}

#on récupère tous les supports des régions concernées
with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:

        for i in range(nbRegions):
            if(int(support[5]) in regions[i]):
                supportRegions[support[0]] = support[5]

with open('../script/tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    #tableau 2D qui représente chaque ville le nombre d'antennes 4G par année pour chaque region
    tabRegion = [[0 for annee in range(nbTranches)] for ville in range(nbRegions)]

    for emetteur in file_readerEme:

        if(emetteur[1] in supportRegions and generation in emetteur[3]):

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

                for j in range(nbRegions):
                    if region in regions[j]:
                        tabRegion[j][tranche] += 1


    index = ["" for i in range(nbTranches)]

    for i in range(1, len(tabAnnee)):
        index[i] = str(tabAnnee[i-1]) +"-"+str(tabAnnee[i])

    index[0] = "<"+str(tabAnnee[0])
    index[nbTranches-1] = ">"+str(tabAnnee[len(tabAnnee)-1])

    data = {}

    for i in range(nbRegions):
        data[nomRegions[i]] = tabRegion[i]

    df = pd.DataFrame(data=data)

    plt.rcParams["figure.figsize"] = figsize

    for i in range(nbRegions):
        df[nomRegions[i]] = df[nomRegions[i]].cumsum()
        nbEmetRegions = [df[nomRegions[j]][len(df[nomRegions[j]]) - 1] for j in range(nbRegions)]
        df[nomRegions[i]] = (df[nomRegions[i]]/nbEmetRegions[i])*100
        plt.plot(index, df[nomRegions[i]], label = nomRegions[i] + ": " + str(nbEmetRegions[i]), marker = markers[i], linestyle = linestyles[i])


    plt.grid(b=True, which='major', axis='both')
    plt.title(titre, fontsize=tailleTitre)
    plt.ylabel(axeOrdonnee, fontsize=tailleOrdonnee)
    plt.xlabel(axeAbscisse, fontsize=tailleAbscisse)
    plt.yticks(np.arange(0, 101, 5.0))

    plt.legend()

    plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/'+texteSauvegarde)
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))