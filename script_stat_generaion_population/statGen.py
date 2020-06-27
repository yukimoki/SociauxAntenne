import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

start_time = time.time()

#represente les tranches de population
tabListPop = [[0, 50], [50, 100], [100, 250], [250, 500], [500, 1000], [1000, 5000], [5000, 10000], [10000, 20000], [20000, 40000], [40000, 60000], [60000, 80000], [100000, 120000], [120000, 140000], [140000, 200000], [200000, 400000], [400000]]

figsize = (12, 10)

tailleTitre = 25

titre = "Nombre d'émetteurs par génération et population"
titreMax = "Nombre d'émetteurs de génération maximale\n et par population"

tailleOrdonnee = 15
tailleAbscisse = 15
texteAbscisse = "Nombre d'habitants (en milliers)"
texteOrdonnee = "Nombre d'émetteurs"

#nb de tranches
nbListPop = len(tabListPop)

setsPopulation  = [set() for i in range(nbListPop)]

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

#dictionnaire l'identifiant d'un support et un tableau de booléen pour chaque génération d'émetteur
dictionnaireSupport = {} #de la forme {id_sup: [Bool, Bool, Bool, Bool]}

with open('../script/tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    tabGen = [False, False, False, False]

    for emetteur in file_readerEme:

        numSup = emetteur[2]

        if("GSM" in emetteur[3]):
            tabGen[0] = True
        elif("UMTS" in emetteur[3]):
            tabGen[1] = True
        elif("LTE" in emetteur[3]):
            tabGen[2] = True
        elif("NG" in emetteur[3]):
            tabGen[3] = True

        if(numSup in dictionnaireSupport):
            
            oldTabGen = dictionnaireSupport[numSup]
            for i in range(4):
                if(tabGen[i]==True or oldTabGen[i]==True):
                    tabGen[i] = True
        
        dictionnaireSupport[numSup] = tabGen
        tabGen = [False, False, False, False]

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
                temp = row[0].split("-")
                for j in temp:
                    setsPopulation[i].add(j)

            elif(habitants>=tabListPop[i][0] and habitants<tabListPop[i][1]):
                trouve = True
                temp = row[0].split("-")
                for j in temp:
                    setsPopulation[i].add(j)
            i += 1

def toutEmetteurConfondus():

    #tableau 2D qui représente chaque génération d'életteurs (2G, 3G, 4G puis 5G)
    tabGeneration = [[0 for compteurPopulation in range(nbListPop)] for generation in range(4)]

    with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        for support in file_readerSup:

            if(support[0] in dictionnaireSupport):
                tabGen = dictionnaireSupport[support[0]]

                i = 0

                trouve = False

                while i < nbListPop and trouve==False:

                    if(setsPopulation[i].__contains__(support[5].replace("'", ""))):
                        trouve = True

                        for generation in range(4):
                            if(tabGen[generation]):
                                tabGeneration[generation][i] += 1

                    i+=1


    data = {
            "2G":tabGeneration[0],
            "3G":tabGeneration[1],
            "4G":tabGeneration[2],
            "5G":tabGeneration[3]
            };


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

    columns = ["2G", "3G", "4G", "5G"]

    dataFrame = pd.DataFrame(data=data, index=index, columns=columns);

    plt.rcParams["figure.figsize"] = figsize
    dataFrame.plot.bar(stacked=True, rot=0, title=titre)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titre, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)

    maxHauteur = 0

    for i in range(nbListPop):
        sumColumn = 0
        for j in range(4):
            sumColumn+= tabGeneration[j][i]
        if(sumColumn>maxHauteur):
            maxHauteur = sumColumn

    plt.yticks(np.arange(0, maxHauteur*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatToutOperateurConfondu/statPopGenTous.png')


def emetteurGenMax():


    tabGeneration = [[0 for i in range(nbListPop)] for j in range(4)]

    with open('../script/tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        for support in file_readerSup:

            if(support[0] in dictionnaireSupport):
                tabGen = dictionnaireSupport[support[0]]

                i = 0

                trouve = False

                while i < nbListPop and trouve==False:

                    if(setsPopulation[i].__contains__(support[5].replace("'", ""))):
                        trouve = True

                        if(tabGen[3]):
                            tabGeneration[3][i] += 1
                        elif(tabGen[2]):
                            tabGeneration[2][i] += 1
                        elif(tabGen[1]):
                            tabGeneration[1][i] += 1
                        elif(tabGen[0]):
                            tabGeneration[0][i] += 1

                    i+=1


    data = {
            "2G":tabGeneration[0],
            "3G":tabGeneration[1],
            "4G":tabGeneration[2],
            "5G":tabGeneration[3]
            };


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

    columns = ["2G", "3G", "4G", "5G"]
    dataFrame = pd.DataFrame(data=data, index=index);

    plt.rcParams["figure.figsize"] = figsize
    dataFrame.plot.bar(stacked=True, rot=0, title=titreMax)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)

    maxHauteur = 0

    for i in range(nbListPop):
        sumColumn = 0
        for j in range(4):
            sumColumn+= tabGeneration[j][i]
        if(sumColumn>maxHauteur):
            maxHauteur = sumColumn

    plt.yticks(np.arange(0, maxHauteur*1.05, 25.0))

    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatToutOperateurConfondu/statPopGenMax.png')


toutEmetteurConfondus()
emetteurGenMax()

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))