import csv
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

start_time = time.time()

#correspond à la 4G dans la table EMETTEUR.csv
generation = "LTE"

figsize = (12, 10)
titre  = "Pourcentage d'émetteurs mis en service par commune et année"
tailleTitre = 25

axeOrdonnee = "Pourcentage d'émetteurs"
axeAbscisse = "Année"
tailleOrdonnee = 15
tailleAbscisse = 15

tabListPop = [[10, 100], [100, 200], [200, 300], [300, 400], [400, 500], [500, 750], [750, 1000], [1000, 2500], [2500, 5000], [5000, 10000], [10000, 25000], [25000, 50000], [50000, 100000], [100000, 250000], [250000]]
tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

linestyles = ["-", "--", "-.", "--", "-", "--", "-.", "--", "-", "--", "--", "-.", "--", "-", "--", "-.", "--", "-", "--"]
markers = ["o", "^", "v", "<", ">", "1", "2","3", "4", "8", "s", "p", "P", "*", "D", "x", "X"]

texteSauvegarde = "statCouvertureTous.png"

nbListPop = len(tabListPop)
setsPopulation  = [set() for i in range(nbListPop)]

nbTranchesAnnee = len(tabAnnee) + 1

#dictionaire dont la clé est l'id du support et la valeur le code postal de la commune dans laquelle il se trouve
codePostauxSupportsConcernees = {} #{id_sup: codepostalsup}

#on récupère les codes postaux des communes et on les mets dans le set de communes en fonction de la population
with open('../script/tables/getPopCodePostal.csv', 'r', encoding='UTF-8', newline='') as file_carre:
    file_reader = csv.reader(file_carre, delimiter=';')
    next(file_reader)

    for line in file_reader:
        habitants = int(line[2])
        i = 0
        trouve = False
        while i < nbListPop and trouve==False:

            if i == nbListPop - 1 and habitants>=tabListPop[i][0]:
                trouve = True
                temp = line[0].split("-")
                for j in temp:
                    setsPopulation[i].add(j)

            elif(habitants>=tabListPop[i][0] and habitants<tabListPop[i][1]):
                trouve = True
                temp = line[0].split("-")
                for j in temp:
                    setsPopulation[i].add(j)
            i += 1

#on récupère tous les supports des communes concernées
with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)
    for support in file_readerSup:
        for i in range(nbListPop):
            codePostauxSupportsConcernees[support[0]] = support[5]

with open('../script/tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    #tableau 2D qui représente le nombre d'antennes 4G par année pour chaque commune
    tabCommunes = [[0 for annee in range(nbTranchesAnnee)] for commune in range(nbListPop)]

    for emetteur in file_readerEme:

        idSup = emetteur[1]

        if(idSup in codePostauxSupportsConcernees and generation in emetteur[3]):

            codePostalSupport = codePostauxSupportsConcernees[idSup]

            dateMiseEnService = emetteur[4]

            if(dateMiseEnService != ''):

                annee = int(dateMiseEnService[6:])

                indiceAnnee = 0

                i = len(tabAnnee) - 1

                trouveAnnee = False

                while i >= 0 and trouveAnnee==False:

                    if(annee >= tabAnnee[i]):
                        trouveAnnee = True
                        indiceAnnee = i + 1

                    i -= 1

                if trouveAnnee == False and annee < tabAnnee[0]:
                    trouveAnnee = True
                    indiceAnnee = 0

                for j in range(nbListPop):
                    if(codePostalSupport in setsPopulation[j] and trouveAnnee):
                        tabCommunes[j][indiceAnnee] += 1

    index = ["" for i in range(nbTranchesAnnee)]

    for i in range(1, len(tabAnnee)):
        if(tabAnnee[i] - tabAnnee[i-1] == 1):
            index[i] = str(tabAnnee[i-1])
        else:
            index[i] = str(tabAnnee[i-1]) +"-"+str(tabAnnee[i])

    index[0] = "<"+str(tabAnnee[0])
    index[nbTranchesAnnee-1] = ">"+str(tabAnnee[len(tabAnnee)-1])

    columns = ["" for i in range(nbListPop)]

    for i in range(nbListPop - 1):
        columns[i] = "communes de " + str(tabListPop[i][0]) +" à "+ str(tabListPop[i][1]  - 1) + " habitants"

    if(len(tabListPop[nbListPop-1]) == 1):
        columns[nbListPop-1] = "communes de plus de "+str(tabListPop[nbListPop-1][0]) + " habitants"
    else:
        columns[nbListPop-1] = "communes de " + str(tabListPop[nbListPop-1][0]) +" à "+ str(tabListPop[nbListPop-1][1] - 1) + " habitants"

    data = {}

    for i in range(nbListPop):
        data[columns[i]] = tabCommunes[i]

    df = pd.DataFrame(data=data)

    plt.rcParams["figure.figsize"] = figsize

    for i in range(nbListPop):
        df[columns[i]] = df[columns[i]].cumsum()
        nbEmetCommunes = [df[columns[j]][len(df[columns[j]]) - 1] for j in range(nbListPop)]
        df[columns[i]] = (df[columns[i]]/nbEmetCommunes[i])*100
        plt.plot(index, df[columns[i]], label = columns[i]+ ": " + str(nbEmetCommunes[i]), marker = markers[i], linestyle = linestyles[i])


    plt.grid(b=True, which='major', axis='both')
    plt.title(titre, fontsize=tailleTitre)
    plt.ylabel(axeOrdonnee, fontsize=tailleOrdonnee)
    plt.xlabel(axeAbscisse, fontsize=tailleAbscisse)
    plt.yticks(np.arange(0, 101, 5.0))

    plt.legend()

    plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/'+texteSauvegarde)
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))