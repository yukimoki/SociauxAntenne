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

axeOrdonnee = "Population"
axeAbscisse = "Année"
tailleOrdonnee = 15
tailleAbscisse = 15

tabAnnee = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

nomsCommunes = ['Chancia', 'Riboux', 'Change', 'Aresches', 'Verrie', 'Zermezeele', 'Vernay', 'Xaintray', 'Yrouerre', 'Saint-Élie']

texteSauvegarde = "statSeuilCommunesRepresentatives.png"

nbCommunes = len(nomsCommunes)
codePostauxCommunes = [[] for i in range(nbCommunes)]
popCommune = [0 for i in range(nbCommunes)]
nbTranches = len(tabAnnee) + 1

#dictionaire dont la clé est l'id du support et la valeur le code postal de la commune dans laquelle il se trouve
codePostauxSupportsConcernees = {} #{id_sup: codepostalsup}

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
                popCommune[i] = int(line[2])

#on récupère tous les supports des communes concernées
with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup:
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)

    for support in file_readerSup:

        for i in range(nbCommunes):
            if(int(support[5]) in codePostauxCommunes[i]):
                codePostauxSupportsConcernees[support[0]] = support[5]

with open('../script/tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    #tableau 2D qui représente le nombre d'antennes 4G par année pour chaque commune
    tabCommunes = [[0 for annee in range(nbTranches)] for commune in range(nbCommunes)]

    for emetteur in file_readerEme:

        if(emetteur[1] in codePostauxSupportsConcernees and generation in emetteur[3]):

            codePostalSupport = int(codePostauxSupportsConcernees[emetteur[1]])

            dateMiseEnService = emetteur[4]

            if(dateMiseEnService != ''):

                annee = int(dateMiseEnService[6:])

                tranche = -1

                i = len(tabAnnee) - 1

                trouve = False

                while i >= 0 and trouve==False:

                    if(annee >= tabAnnee[i]):
                        trouve = True
                        tranche = i + 1

                    i -= 1

                if trouve == False and annee < tabAnnee[0]:
                    tranche = 0

                for j in range(nbCommunes):
                    if codePostalSupport in codePostauxCommunes[j] and tranche!=-1:
                        tabCommunes[j][tranche] += 1


    index = ["" for i in range(nbTranches)]

    for i in range(1, len(tabAnnee)):
        if(tabAnnee[i] - tabAnnee[i-1] == 1):
            index[i] = str(tabAnnee[i-1])
        else:
            index[i] = str(tabAnnee[i-1]) +"-"+str(tabAnnee[i])

    index[0] = "<"+str(tabAnnee[0])
    index[nbTranches-1] = ">"+str(tabAnnee[len(tabAnnee)-1])

    #on fait la somme cumulatif puis le pourcentage pour chaque commune
    for i in  range(nbCommunes):
        #somme cumulative
        for j in range(1, nbTranches):
            tabCommunes[i][j] += tabCommunes[i][j-1]

        #pourcentage
        for j in range(nbTranches):
            tabCommunes[i][j] = (tabCommunes[i][j]/tabCommunes[i][nbTranches-1]) * 100

    #tableau qui contient l'indice pour chaque commune où le seuil à été atteint
    tabAnneSeuil = [0 for i in range(nbCommunes)]
    tabPourcentSeuil = [0 for i in range(nbCommunes)]

    for i in range(nbCommunes):
        temp = tabCommunes[i]
        indiceSeuilAtteint = 0
        trouveSeuil = False 
        j = 0
        while j < nbTranches and trouveSeuil == False:
            if(temp[j]>=seuil):
                indiceSeuilAtteint = j
                tabPourcentSeuil[i] = temp[j]
                trouveSeuil = True
            j += 1

        tabAnneSeuil[i] = indiceSeuilAtteint

    anneeMin = min(tabAnneSeuil)
    anneeMax = max(tabAnneSeuil)

    anneeCommune = [index[tabAnneSeuil[i]] for i in range(nbCommunes)]

    dataSeuil = {}


    rang = 0

    dictAnneeRang = {}

    for i in range(anneeMin, anneeMax+1):
        dictAnneeRang[index[i]] = rang
        rang +=1

    rangAnnee = [dictAnneeRang[anneeCommune[i]] for i in range(nbCommunes)]

    dataSeuil["nomCommune"] = nomsCommunes
    dataSeuil["population"] = popCommune
    dataSeuil["annee"] = anneeCommune
    dataSeuil["rangAnnee"] = rangAnnee
    dataSeuil["pourcentAtteint"] = tabPourcentSeuil

    plt.rcParams["figure.figsize"] = figsize

    df = pd.DataFrame(data=dataSeuil).sort_values(by=["rangAnnee"], ascending=True)

    for index, row in df.iterrows():
        for i in range(nbCommunes):
            if(row["nomCommune"]==nomsCommunes[i]):
                codePostal = ", " + str(codePostauxCommunes[i][0])[0:2]
                textLabel = nomsCommunes[i]+ codePostal + ": " + str(row["population"])
        plt.plot(row["annee"], row["population"], 'x-', label = textLabel)

    plt.grid(b=True, which='major', axis='both')
    plt.title(titre, fontsize=tailleTitre)
    plt.ylabel(axeOrdonnee, fontsize=tailleOrdonnee)
    plt.xlabel(axeAbscisse, fontsize=tailleAbscisse)

    def label_point(x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            ax.text(point['x'], point['y'], str(point['val']))

    label_point(df.annee, df.population, df.nomCommune, plt)

    plt.legend()

    plt.savefig('../statistiques/emetteur_population_support/StatParAnnee/'+texteSauvegarde)
    

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))