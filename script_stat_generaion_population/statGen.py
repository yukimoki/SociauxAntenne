import csv
import pandas as pd
import matplotlib.pyplot as plot
import sys
import time

start_time = time.time()

listInf05M = set() #len = 18 403

listInf1M = set() #len = 6 672

listInf5M = set() #len = 7 713

listInf10M = set() #len = 1 181

listInf20M = set() #len = 524

listInf40M = set() #len = 278

listInf60M =set() #len = 93

listInf80M = set() #len = 34

listInf100M = set() #len = 17

listInf140M = set() #len = 18

listSup140M = set() #len = 24

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
        if(int(row[2])>140000):
            temp = row[0].split(",")
            for i in temp:
                listSup140M.add(i)
        elif(int(row[2])>100000):
            temp = row[0].split(",")
            for i in temp:
                listInf140M.add(i)
        elif(int(row[2])>80000):
            temp = row[0].split(",")
            for i in temp:
                listInf100M.add(i)
        elif(int(row[2])>60000):
            temp = row[0].split(",")
            for i in temp:
                listInf80M.add(i)
        elif(int(row[2])>40000):
            temp = row[0].split(",")
            for i in temp:
                listInf60M.add(i)
        elif(int(row[2])>20000):
            temp = row[0].split(",")
            for i in temp:
                listInf40M.add(i)
        elif(int(row[2])>10000):
            temp = row[0].split(",")
            for i in temp:
                listInf20M.add(i)
        elif(int(row[2])>5000):
            temp = row[0].split(",")
            for i in temp:
                listInf10M.add(i)
        elif(int(row[2])>1000):
            temp = row[0].split(",")
            for i in temp:
                listInf5M.add(i)
        elif(int(row[2])>500):
            temp = row[0].split(",")
            for i in temp:
                listInf1M.add(i)
        else:
            temp = row[0].split(",")
            for i in temp:
                listInf05M.add(i)

def toutEmetteurConfondus():

    gen2G = [0,0,0,0,0,0,0,0,0,0,0]
    gen3G = [0,0,0,0,0,0,0,0,0,0,0]
    gen4G = [0,0,0,0,0,0,0,0,0,0,0]
    gen5G = [0,0,0,0,0,0,0,0,0,0,0]


    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        for support in file_readerSup:

            if(support[0] in d):
                tabGen = d[support[0]]
                
                if(listInf05M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[0] += 1
                    if(tabGen[1]):
                        gen3G[0] += 1
                    if(tabGen[2]):
                        gen4G[0] += 1
                    if(tabGen[3]):
                        gen5G[0] += 1
                elif(listInf1M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[1] += 1
                    if(tabGen[1]):
                        gen3G[1] += 1
                    if(tabGen[2]):
                        gen4G[1] += 1
                    if(tabGen[3]):
                        gen5G[1] += 1
                elif(listInf5M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[2] += 1
                    if(tabGen[1]):
                        gen3G[2] += 1
                    if(tabGen[2]):
                        gen4G[2] += 1
                    if(tabGen[3]):
                        gen5G[2] += 1
                elif(listInf10M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[3] += 1
                    if(tabGen[1]):
                        gen3G[3] += 1
                    if(tabGen[2]):
                        gen4G[3] += 1
                    if(tabGen[3]):
                        gen5G[3] += 1
                elif(listInf20M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[4] += 1
                    if(tabGen[1]):
                        gen3G[4] += 1
                    if(tabGen[2]):
                        gen4G[4] += 1
                    if(tabGen[3]):
                        gen5G[4] += 1
                elif(listInf40M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[5] += 1
                    if(tabGen[1]):
                        gen3G[5] += 1
                    if(tabGen[2]):
                        gen4G[5] += 1
                    if(tabGen[3]):
                        gen5G[5] += 1
                elif(listInf60M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[6] += 1
                    if(tabGen[1]):
                        gen3G[6] += 1
                    if(tabGen[2]):
                        gen4G[6] += 1
                    if(tabGen[3]):
                        gen5G[6] += 1
                elif(listInf80M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[7] += 1
                    if(tabGen[1]):
                        gen3G[7] += 1
                    if(tabGen[2]):
                        gen4G[7] += 1
                    if(tabGen[3]):
                        gen5G[7] += 1
                elif(listInf100M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[8] += 1
                    if(tabGen[1]):
                        gen3G[8] += 1
                    if(tabGen[2]):
                        gen4G[8] += 1
                    if(tabGen[3]):
                        gen5G[8] += 1
                elif(listInf140M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[9] += 1
                    if(tabGen[1]):
                        gen3G[9] += 1
                    if(tabGen[2]):
                        gen4G[9] += 1
                    if(tabGen[3]):
                        gen5G[9] += 1
                elif(listSup140M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[0]):
                        gen2G[10] += 1
                    if(tabGen[1]):
                        gen3G[10] += 1
                    if(tabGen[2]):
                        gen4G[10] += 1
                    if(tabGen[3]):
                        gen5G[10] += 1


    data = {
            "2G":gen2G,
            "3G":gen3G,
            "4G":gen4G,
            "5G":gen5G
            };

    index = ["0-0.5", "0.5-1", "1-5", "5-10", "10-20", "20-40", "40-60", "60-80", "80-100", "100-140", ">140"]
    columns = ["2G", "3G", "4G", "5G"]

    dataFrame = pd.DataFrame(data=data, index=index, columns=columns);

    dataFrame.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatToutOperateurConfondu/statPopGenTous.png')


def emetteurGenMax():


    gen2G = [0,0,0,0,0,0,0,0,0,0,0]
    gen3G = [0,0,0,0,0,0,0,0,0,0,0]
    gen4G = [0,0,0,0,0,0,0,0,0,0,0]
    gen5G = [0,0,0,0,0,0,0,0,0,0,0]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        for support in file_readerSup:

            if(support[0].replace("'","") in d):
                tabGen = d[support[0].replace("'","")]
                
                if(listInf05M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[0] += 1
                    elif(tabGen[2]):
                        gen4G[0] += 1
                    elif(tabGen[1]):
                        gen3G[0] += 1
                    elif(tabGen[0]):
                        gen2G[0] += 1
                elif(listInf1M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[1] += 1
                    elif(tabGen[2]):
                        gen4G[1] += 1
                    elif(tabGen[1]):
                        gen3G[1] += 1
                    elif(tabGen[0]):
                        gen2G[1] += 1
                elif(listInf5M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[2] += 1
                    elif(tabGen[2]):
                        gen4G[2] += 1
                    elif(tabGen[1]):
                        gen3G[2] += 1
                    elif(tabGen[0]):
                        gen2G[2] += 1
                elif(listInf10M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[3] += 1
                    elif(tabGen[2]):
                        gen4G[3] += 1
                    elif(tabGen[1]):
                        gen3G[3] += 1
                    elif(tabGen[0]):
                        gen2G[3] += 1
                elif(listInf20M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[4] += 1
                    elif(tabGen[2]):
                        gen4G[4] += 1
                    elif(tabGen[1]):
                        gen3G[4] += 1
                    elif(tabGen[0]):
                        gen2G[4] += 1
                elif(listInf40M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[5] += 1
                    elif(tabGen[2]):
                        gen4G[5] += 1
                    elif(tabGen[1]):
                        gen3G[5] += 1
                    elif(tabGen[0]):
                        gen2G[5] += 1
                elif(listInf60M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[6] += 1
                    elif(tabGen[2]):
                        gen4G[6] += 1
                    elif(tabGen[1]):
                        gen3G[6] += 1
                    elif(tabGen[0]):
                        gen2G[6] += 1
                elif(listInf80M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[7] += 1
                    elif(tabGen[2]):
                        gen4G[7] += 1
                    elif(tabGen[1]):
                        gen3G[7] += 1
                    elif(tabGen[0]):
                        gen2G[7] += 1
                elif(listInf100M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[8] += 1
                    elif(tabGen[2]):
                        gen4G[8] += 1
                    elif(tabGen[1]):
                        gen3G[8] += 1
                    elif(tabGen[0]):
                        gen2G[8] += 1
                elif(listInf140M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[9] += 1
                    elif(tabGen[2]):
                        gen4G[9] += 1
                    elif(tabGen[1]):
                        gen3G[9] += 1
                    elif(tabGen[0]):
                        gen2G[9] += 1
                elif(listSup140M.__contains__(support[5].replace("'", ""))):
                    if(tabGen[3]):
                        gen5G[10] += 1
                    elif(tabGen[2]):
                        gen4G[10] += 1
                    elif(tabGen[1]):
                        gen3G[10] += 1
                    elif(tabGen[0]):
                        gen2G[10] += 1


    data = {
            "2G":gen2G,
            "3G":gen3G,
            "4G":gen4G,
            "5G":gen5G
            };

    index = ["0-0.5", "0.5-1", "1-5", "5-10", "10-20", "20-40", "40-60", "60-80", "80-100", "100-140", ">140"]
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