import csv
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
from datetime import datetime

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

tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

nomsCommunes = ["Fort-de-France", "Arvieu", "Bozouls", "Les Eyzies"]
codePostauxCommunes = [[] for i in range(len(nomsCommunes))]
linestyles = ["-", "--", "-.", "--"]
markers = ["o", "o", "o","p"]

texteSauvegarde = "statCommunsEmetAncienFABL.png"

nbCommunes = len(nomsCommunes)

nbTranchesAnnee = len(tabAnnee) + 1

codePostauxSupportsConcernees = {}

premierEmetteurParSupport = {}

#on récupère les codes postaux des communes
with open('../script/tables/getPopCodePostal.csv', 'r', encoding='UTF-8', newline='') as file_carre:
    file_reader = csv.reader(file_carre, delimiter=';')
    next(file_reader)

    for line in file_reader:
        nom = line[1]

        for i in range(nbCommunes):
            if(nom == nomsCommunes[i]):
                stringCodePostal = line[0].split("-")
                intCP = [int(i) for i in stringCodePostal]
                codePostauxCommunes[i] = intCP

#on récupère tous les supports des communes concernées
with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:

        for i in range(nbCommunes):
            if(int(support[5]) in codePostauxCommunes[i]):
                codePostauxSupportsConcernees[support[0]] = support[5]

#on récupère pour chaque support l'émetteur 4G le plus ancien
with open('../script/tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    for emetteur in file_readerEme:

        idSup = emetteur[1]

        if(idSup in codePostauxSupportsConcernees and generation in emetteur[3]):

            dateMiseEnService = emetteur[4]

            if(dateMiseEnService != ''):

                annee = int(dateMiseEnService[6:])

                if(idSup in premierEmetteurParSupport):
                    oldAnnee = int(premierEmetteurParSupport[idSup])

                    if oldAnnee > annee:
                        premierEmetteurParSupport[idSup] = dateMiseEnService[6:]
                else:
                    premierEmetteurParSupport[idSup] = dateMiseEnService[6:]

    
#tableau 2D qui représente le nombre d'antennes 4G par année pour chaque commune
tabCommunes = [[0 for annee in range(nbTranchesAnnee)] for commune in range(nbCommunes)]

for key in premierEmetteurParSupport:

    idSup = key

    codePostalSupport = int(codePostauxSupportsConcernees[idSup])

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

    for j in range(nbCommunes):
        if codePostalSupport in codePostauxCommunes[j]:
            tabCommunes[j][tranche] += 1


index = ["" for i in range(nbTranchesAnnee)]

for i in range(1, len(tabAnnee)):
    index[i] = str(tabAnnee[i-1]) +"-"+str(tabAnnee[i])

index[0] = "<"+str(tabAnnee[0])
index[nbTranchesAnnee-1] = ">"+str(tabAnnee[len(tabAnnee)-1])

data = {}

for i in range(nbCommunes):
    data[nomsCommunes[i]] = tabCommunes[i]

df = pd.DataFrame(data=data)

plt.rcParams["figure.figsize"] = figsize

for i in range(nbCommunes):
    df[nomsCommunes[i]] = df[nomsCommunes[i]].cumsum()
    nbEmetCommunes = [df[nomsCommunes[j]][len(df[nomsCommunes[j]]) - 1] for j in range(nbCommunes)]
    df[nomsCommunes[i]] = (df[nomsCommunes[i]]/nbEmetCommunes[i])*100
    codePostal = ", " + str(codePostauxCommunes[i][0])[0:2]
    plt.plot(index, df[nomsCommunes[i]], label = nomsCommunes[i]+ codePostal + ": " + str(nbEmetCommunes[i]), marker = markers[i], linestyle = linestyles[i])


plt.grid(b=True, which='major', axis='both')
plt.title(titre, fontsize=tailleTitre)
plt.ylabel(axeOrdonnee, fontsize=tailleOrdonnee)
plt.xlabel(axeAbscisse, fontsize=tailleAbscisse)
plt.yticks(np.arange(0, 101, 5.0))

plt.legend()
plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/'+texteSauvegarde)
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))