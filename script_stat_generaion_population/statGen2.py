import csv
import pandas as pd
import matplotlib.pyplot as plot
import sys
import time

start_time = time.time()

tabListPop = [50, 100, 250, 500, 1000, 5000, 10000, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 200000, 400000]

nbListPop = len(tabListPop)

setsPopulation  = [set() for i in range(nbListPop)]

#dictionnaire qui contient toutes les stations et un tableau de booléen pour chaque génération d'emetteur 
d = {}

with open('../tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    numSup = -1
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

        if(numSup in d):
            
            oldTabGen = d[numSup]
            for i in range(4):
                if(tabGen[i]==True or oldTabGen[i]==True):
                    tabGen[i] = True
        
        d[numSup] = tabGen
        tabGen = [False, False, False, False]

with open('../tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
    file_reader = csv.reader(File, delimiter=';')
    next(file_reader)
    for row in file_reader:

        i = nbListPop - 1

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

def toutEmetteurConfondus():

    tabGeneration = [[0 for i in range(nbListPop)] for j in range(4)]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        for support in file_readerSup:

            if(support[0] in d):
                tabGen = d[support[0]]

                i = 0

                trouve = False

                while i < nbListPop and trouve==False:

                    if(setsPopulation[i].__contains__(support[5].replace("'", ""))):
                        trouve = True

                        if(tabGen[0]):
                            tabGeneration[0][i] += 1
                        if(tabGen[1]):
                            tabGeneration[1][i] += 1
                        if(tabGen[2]):
                            tabGeneration[2][i] += 1
                        if(tabGen[3]):
                            tabGeneration[3][i] += 1

                    i+=1

                if trouve == False:
                    if(tabGen[0]):
                        tabGeneration[0][nbListPop - 1] += 1
                    if(tabGen[1]):
                        tabGeneration[1][nbListPop - 1] += 1
                    if(tabGen[2]):
                        tabGeneration[2][nbListPop - 1] += 1
                    if(tabGen[3]):
                        tabGeneration[3][nbListPop - 1] += 1


    data = {
            "2G":tabGeneration[0],
            "3G":tabGeneration[1],
            "4G":tabGeneration[2],
            "5G":tabGeneration[3]
            };

    index = ["<"+str(tabListPop[i]/1000) for i in range(nbListPop)]
    columns = ["2G", "3G", "4G", "5G"]

    dataFrame = pd.DataFrame(data=data, index=index, columns=columns);

    dataFrame.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatToutOperateurConfondu/statPopGenTous.png')


def emetteurGenMax():


    tabGeneration = [[0 for i in range(nbListPop)] for j in range(4)]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        for support in file_readerSup:

            if(support[0] in d):
                tabGen = d[support[0]]

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

                if trouve == False:
                    if(tabGen[3]):
                        tabGeneration[3][nbListPop - 1] += 1
                    elif(tabGen[2]):
                        tabGeneration[2][nbListPop - 1] += 1
                    elif(tabGen[1]):
                        tabGeneration[1][nbListPop - 1] += 1
                    elif(tabGen[0]):
                        tabGeneration[0][nbListPop - 1] += 1


    data = {
            "2G":tabGeneration[0],
            "3G":tabGeneration[1],
            "4G":tabGeneration[2],
            "5G":tabGeneration[3]
            };

    index = ["<"+str(tabListPop[i]/1000) for i in range(nbListPop)]
    columns = ["2G", "3G", "4G", "5G"]
    dataFrame = pd.DataFrame(data=data, index=index);

    dataFrame.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs de génération max/support et population")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatToutOperateurConfondu/statPopGenMax.png')


toutEmetteurConfondus()
emetteurGenMax()

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))