import csv
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np

start_time = time.time()

#correspond à la 4G dans la table EMETTEUR.csv
generation = "LTE"
#seuil en pourcentage
seuil = 50

figsize = (12, 10)
titre  = "Année où le seuil de " + str(seuil) + "% d'émetteurs à été atteint par commune"
tailleTitre = 20

axeOrdonnee = "Pourcent atteint"
axeAbscisse = "Année"
tailleOrdonnee = 15
tailleAbscisse = 15

tabListPop = [[10, 100], [100, 200], [200, 300], [300, 400], [400, 500], [500, 750], [750, 1000], [1000, 2500], [2500, 5000], [5000, 10000], [10000, 25000], [25000, 50000], [50000, 100000], [100000, 250000], [250000]]
tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
markers = ["o", "^", "v", "<", ">", "1", "2","3", "4", "8", "s", "d", "P", "*", "*", "x", "X"]

texteSauvegarde = "statSeuilTous.png"

nbListPop = len(tabListPop)
setsPopulation  = [set() for i in range(nbListPop)]
popCommune = [0 for i in range(nbListPop)]
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
                if(popCommune[i] == 0):
                    popCommune[i] = habitants
                else:
                    popCommune[i] = (popCommune[i] + habitants)/2

            elif(habitants>=tabListPop[i][0] and habitants<tabListPop[i][1]):
                trouve = True
                temp = line[0].split("-")
                for j in temp:
                    setsPopulation[i].add(j)
                if(popCommune[i] == 0):
                    popCommune[i] = habitants
                else:
                    popCommune[i] = (popCommune[i] + habitants)/2
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
        columns[i] = "communes de " + str(tabListPop[i][0]) +" à "+ str(tabListPop[i][1]-1) + " habitants"

    if(len(tabListPop[nbListPop-1]) == 1):
        columns[nbListPop-1] = "communes de plus de "+str(tabListPop[nbListPop-1][0]) + " habitants"
    else:
        columns[nbListPop-1] = "communes de " + str(tabListPop[nbListPop-1][0]) +" à "+ str(tabListPop[nbListPop-1][1]-1) + " habitants"

    #on fait la somme cumulatif puis le pourcentage pour chaque commune
    for i in  range(nbListPop):
        #somme cumulative
        for j in range(1, nbTranchesAnnee):
            tabCommunes[i][j] += tabCommunes[i][j-1]

        #pourcentage
        for j in range(nbTranchesAnnee):
            tabCommunes[i][j] = (tabCommunes[i][j]/tabCommunes[i][nbTranchesAnnee-1]) * 100

    #tableau qui contient l'indice pour chaque commune où le seuil à été atteint
    tabAnneSeuil = [0 for i in range(nbListPop)]
    tabPourcentSeuil = [0 for i in range(nbListPop)]

    for i in range(nbListPop):
        temp = tabCommunes[i]
        indiceSeuilAtteint = 0
        trouveSeuil = False 
        j = 0
        while j < nbTranchesAnnee and trouveSeuil == False:
            if(temp[j]>=seuil):
                indiceSeuilAtteint = j
                tabPourcentSeuil[i] = temp[j]
                trouveSeuil = True
            j += 1

        tabAnneSeuil[i] = indiceSeuilAtteint

    anneeMin = min(tabAnneSeuil)
    anneeMax = max(tabAnneSeuil)

    anneeCommune = [index[tabAnneSeuil[i]] for i in range(nbListPop)]

    dataSeuil = {}

    rang = 0

    dictAnneeRang = {}

    for i in range(anneeMin, anneeMax+1):
        dictAnneeRang[index[i]] = rang
        rang +=1

    rangAnnee = [dictAnneeRang[anneeCommune[i]] for i in range(nbListPop)]

    dataSeuil["coulmn"] = columns
    dataSeuil["population"] = popCommune
    dataSeuil["annee"] = anneeCommune
    dataSeuil["rangAnnee"] = rangAnnee
    dataSeuil["pourcentAtteint"] = tabPourcentSeuil

    plt.rcParams["figure.figsize"] = figsize

    df = pd.DataFrame(data=dataSeuil).sort_values(by=["rangAnnee"], ascending=True)

    for index, row in df.iterrows():
        for i in range(nbListPop):
            if(row["coulmn"]==columns[i]):
                textLabel = columns[i]+ ": " + str(round(row["population"]))
        plt.plot(row["annee"], row["pourcentAtteint"], markers[index], label = textLabel)

    plt.grid(b=True, which='major', axis='both')
    plt.title(titre, fontsize=tailleTitre)
    plt.ylabel(axeOrdonnee, fontsize=tailleOrdonnee)
    plt.xlabel(axeAbscisse, fontsize=tailleAbscisse)

    plt.legend()

    plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/'+texteSauvegarde)
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))