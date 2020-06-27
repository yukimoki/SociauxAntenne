import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import time
import os

start_time = time.time()

#represente les tranches de population
tabListPop = [[0, 50], [50, 100], [100, 250], [250, 500], [500, 1000], [1000, 5000], [5000, 10000], [10000, 20000], [20000, 40000], [40000, 60000], [60000, 80000], [100000, 120000], [120000, 140000], [140000, 200000], [200000, 400000], [400000]]

figsize = (12, 10)

tailleTitre = 25

titreGraphCommun = "Nombre d'émetteurs par génération, population et opérateur"
titreGraphCommunMax = "Nombre d'émetteurs de génération maximale\npar population et opérateur"
titreFreeMax = "Nombre d'émetteurs de génération maximale\nde Free Mobile"
titreFree = "Nombre d'émetteurs par génération et population \nde Free Mobile"
titreSFRMax = "Nombre d'émetteurs de génération maximale\nde SFR"
titreSFR = "Nombre d'émetteurs par génération et population \nde SFR"
titreOrangeMax = "Nombre d'émetteurs de génération maximale\nd'Orange"
titreOrange = "Nombre d'émetteurs par génération et population \nd'Orange"
titreBouyguesMax = "Nombre d'émetteurs de génération maximale\nde Bouygues Télécom"
titreBouygues = "Nombre d'émetteurs par génération et population \nde Bouygues Télecom"

tailleOrdonnee = 15
tailleAbscisse = 15
texteAbscisse = "Nombre d'habitants (en milliers)"
texteOrdonnee = "Nombre d'émetteurs"

nbListPop = len(tabListPop)

setsPopulation  = [set() for i in range(nbListPop)]

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

#fonction qui génère un graph avec plusieur bar entassé
def plot_clustered_stacked(dfall, labels=None, filename="stat.png", title="titre",  H="/", maxi = 0, **kwargs):

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)

    plt.clf()
    
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True, rot = 0,
                      ax=axe,
                      legend=False,
                      grid=True,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    axe.set_title(title, fontsize = tailleTitre)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)

    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    if(maxi != 0):
        plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.tight_layout()
    plt.savefig(filename)


#dictionnaire qui contient toutes les stations et un tableau de booléen pour chaque génération d'emetteur 
dictionnaireSupport = {}

with open('../tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    #represente pour chaque support les générations des emetteur présent et les fournissuers qui les proposent
    #l'ordre est le suivant 2G, 3G, 4G, 5G pour Free puis pour SFR, Orange et Bouygues
    tabEmetGenOper = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

    for emetteur in file_readerEme:

        numSup = emetteur[2]

        i = 0

        if("FREE" in emetteur[5]):
            i = 0
        if("SFR" in emetteur[5]):
            i = 1
        if("ORANGE" in emetteur[5]):
            i = 2
        if("BOUYGUES" in emetteur[5]):
            i = 3

        if("GSM" in emetteur[3]):
            tabEmetGenOper[i*4] = True
        elif("UMTS" in emetteur[3]):
            tabEmetGenOper[i*4+1] = True
        elif("LTE" in emetteur[3]):
            tabEmetGenOper[i*4+2] = True
        elif("NG" in emetteur[3]):
            tabEmetGenOper[i*4+3] = True

        if(numSup in dictionnaireSupport):
            
            oldtabEmetGenOper = dictionnaireSupport[numSup]
            for i in range(16):
                if(tabEmetGenOper[i]==True or oldtabEmetGenOper[i]==True):
                    tabEmetGenOper[i] = True
        
        dictionnaireSupport[numSup] = tabEmetGenOper
        tabEmetGenOper = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

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

    #tableau qui contient pour les opérateurs (Free, SFR, Orange puis Bouygues) un tableau par génération (2,3,4 puis 5G) de compteur de population dans la liste tabListPop
    tabGenerationOperateur = [[[0 for compteurPopulation in range(nbListPop)] for generation in range(4)] for operateur in range(4)]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        #pour chaque support
        for support in file_readerSup:

            #on regarde si le support est présent dans le dictionnaire
            if(support[0] in dictionnaireSupport):
                tabEmetGenOper = dictionnaireSupport[support[0]]

                i = 0

                trouve = False

                while i < nbListPop and trouve==False:

                    if(setsPopulation[i].__contains__(support[5].replace("'", ""))):
                        trouve = True

                        for operateur in range(4):
                            if(tabEmetGenOper[operateur*4]):
                                tabGenerationOperateur[operateur][0][i]+=1
                            if(tabEmetGenOper[operateur*4 + 1]):
                                tabGenerationOperateur[operateur][1][i]+=1
                            if(tabEmetGenOper[operateur*4 + 2]):
                                tabGenerationOperateur[operateur][2][i]+=1
                            if(tabEmetGenOper[operateur*4 + 3]):
                                tabGenerationOperateur[operateur][3][i]+=1

                    i+=1


    dataFree = {
            "2G":tabGenerationOperateur[0][0],
            "3G":tabGenerationOperateur[0][1],
            "4G":tabGenerationOperateur[0][2],
            "5G":tabGenerationOperateur[0][3]
            };

    dataSFR = {
            "2G":tabGenerationOperateur[1][0],
            "3G":tabGenerationOperateur[1][1],
            "4G":tabGenerationOperateur[1][2],
            "5G":tabGenerationOperateur[1][3]
            };

    dataOrange = {
            "2G":tabGenerationOperateur[2][0],
            "3G":tabGenerationOperateur[2][1],
            "4G":tabGenerationOperateur[2][2],
            "5G":tabGenerationOperateur[2][3]
            };

    dataBouygues = {
            "2G":tabGenerationOperateur[3][0],
            "3G":tabGenerationOperateur[3][1],
            "4G":tabGenerationOperateur[3][2],
            "5G":tabGenerationOperateur[3][3]
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

    tabNbEmeFree = [0 for i in range(nbListPop)]
    tabNbEmeSFR = [0 for i in range(nbListPop)]
    tabNbEmeOrange = [0 for i in range(nbListPop)]
    tabNbEmeBouygues = [0 for i in range(nbListPop)]

    for i in range(nbListPop):
        tabNbEmeFree[i]= tabGenerationOperateur[0][0][i] + tabGenerationOperateur[0][1][i] + tabGenerationOperateur[0][2][i] + tabGenerationOperateur[0][3][i]
        tabNbEmeSFR[i]= tabGenerationOperateur[1][0][i] + tabGenerationOperateur[1][1][i] + tabGenerationOperateur[1][2][i] + tabGenerationOperateur[1][3][i]
        tabNbEmeOrange[i]= tabGenerationOperateur[2][0][i] + tabGenerationOperateur[2][1][i] + tabGenerationOperateur[2][2][i] + tabGenerationOperateur[2][3][i]
        tabNbEmeBouygues[i]= tabGenerationOperateur[3][0][i] + tabGenerationOperateur[3][1][i] + tabGenerationOperateur[3][2][i] + tabGenerationOperateur[3][3][i]

    maxF = max(tabNbEmeFree)
    maxS = max(tabNbEmeSFR)
    maxO = max(tabNbEmeOrange)
    maxB = max(tabNbEmeBouygues)

    maxi = max([maxB, maxF, maxS, maxO])

    dfFree = pd.DataFrame(data=dataFree, index=index, columns=columns);
    dfSFR = pd.DataFrame(data=dataSFR, index=index, columns=columns);
    dfOrange = pd.DataFrame(data=dataOrange, index=index, columns=columns);
    dfBouygues = pd.DataFrame(data=dataBouygues, index=index, columns=columns);

    #sauvegarde de tous les graphiques en proportion de leur ordonné maximum
    plt.rcParams["figure.figsize"] = figsize
    dfFree.plot.bar(stacked=True, rot = 0, title=titreFree)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreFree, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxF*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousFree.png')
    


    plt.rcParams["figure.figsize"] = figsize
    dfSFR.plot.bar(stacked=True, rot = 0, title=titreSFR)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreSFR, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxS*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousSFR.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfBouygues.plot.bar(stacked=True, rot = 0, title=titreBouygues)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreBouygues, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxB*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousBouygues.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfOrange.plot.bar(stacked=True, rot = 0, title=titreOrange)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreOrange, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxO*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousOrange.png')
    


    #sauvegarde de tout les graphiques en fonction de l'ordonné maximale de tout les graphes
    plt.rcParams["figure.figsize"] = figsize
    dfFree.plot.bar(stacked=True, rot = 0, title=titreFree)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreFree, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousFree.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfSFR.plot.bar(stacked=True, rot = 0, title=titreSFR)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreSFR, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousSFR.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfBouygues.plot.bar(stacked=True, rot = 0, title=titreBouygues)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreBouygues, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousBouygues.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfOrange.plot.bar(stacked=True, rot = 0, title=titreOrange)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreOrange, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousOrange.png')
    

    plot_clustered_stacked([dfFree, dfSFR, dfOrange, dfBouygues],["Free Mobile", "SFR", "Orange", "Bouygues Télécom"], filename = '../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenOperateurTous.png', title  = titreGraphCommun, maxi = maxi)


def emetteurGenMax():

    #tableau qui contient pour les opérateurs (Free, SFR, Orange puis Bouygues) un tableau par génération (2,3,4 puis 5G) de compteur de population dans la liste tabListPop
    tabGenerationOperateur = [[[0 for compteurPopulation in range(nbListPop)] for generation in range(4)] for operateur in range(4)]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        #pour chaque support
        for support in file_readerSup:

            #on regarde si le support est présent dans le dictionnaire
            if(support[0] in dictionnaireSupport):
                tabEmetGenOper = dictionnaireSupport[support[0]]
                
                i = 0

                trouve = False

                while i < nbListPop and trouve==False:

                    if(setsPopulation[i].__contains__(support[5].replace("'", ""))):
                        trouve = True

                        for operateur in range(4):
                            if(tabEmetGenOper[operateur*4 + 3]):
                                tabGenerationOperateur[operateur][3][i]+=1
                            elif(tabEmetGenOper[operateur*4 + 2]):
                                tabGenerationOperateur[operateur][2][i]+=1
                            elif(tabEmetGenOper[operateur*4 + 1]):
                                tabGenerationOperateur[operateur][1][i]+=1
                            elif(tabEmetGenOper[operateur*4]):
                                tabGenerationOperateur[operateur][0][i]+=1

                    i+=1


    dataFree = {
            "2G":tabGenerationOperateur[0][0],
            "3G":tabGenerationOperateur[0][1],
            "4G":tabGenerationOperateur[0][2],
            "5G":tabGenerationOperateur[0][3]
            };

    dataSFR = {
            "2G":tabGenerationOperateur[1][0],
            "3G":tabGenerationOperateur[1][1],
            "4G":tabGenerationOperateur[1][2],
            "5G":tabGenerationOperateur[1][3]
            };

    dataOrange = {
            "2G":tabGenerationOperateur[2][0],
            "3G":tabGenerationOperateur[2][1],
            "4G":tabGenerationOperateur[2][2],
            "5G":tabGenerationOperateur[2][3]
            };

    dataBouygues = {
            "2G":tabGenerationOperateur[3][0],
            "3G":tabGenerationOperateur[3][1],
            "4G":tabGenerationOperateur[3][2],
            "5G":tabGenerationOperateur[3][3]
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

    tabNbEmeFree = [0 for i in range(nbListPop)]
    tabNbEmeSFR = [0 for i in range(nbListPop)]
    tabNbEmeOrange = [0 for i in range(nbListPop)]
    tabNbEmeBouygues = [0 for i in range(nbListPop)]

    for i in range(nbListPop):
        tabNbEmeFree[i]= tabGenerationOperateur[0][0][i] + tabGenerationOperateur[0][1][i] + tabGenerationOperateur[0][2][i] + tabGenerationOperateur[0][3][i]
        tabNbEmeSFR[i]= tabGenerationOperateur[1][0][i] + tabGenerationOperateur[1][1][i] + tabGenerationOperateur[1][2][i] + tabGenerationOperateur[1][3][i]
        tabNbEmeOrange[i]= tabGenerationOperateur[2][0][i] + tabGenerationOperateur[2][1][i] + tabGenerationOperateur[2][2][i] + tabGenerationOperateur[2][3][i]
        tabNbEmeBouygues[i]= tabGenerationOperateur[3][0][i] + tabGenerationOperateur[3][1][i] + tabGenerationOperateur[3][2][i] + tabGenerationOperateur[3][3][i]

    maxF = max(tabNbEmeFree)
    maxS = max(tabNbEmeSFR)
    maxO = max(tabNbEmeOrange)
    maxB = max(tabNbEmeBouygues)

    maxi = max([maxB, maxF, maxS, maxO])

    dfFree = pd.DataFrame(data=dataFree, index=index, columns=columns);
    dfSFR = pd.DataFrame(data=dataSFR, index=index, columns=columns);
    dfOrange = pd.DataFrame(data=dataOrange, index=index, columns=columns);
    dfBouygues = pd.DataFrame(data=dataBouygues, index=index, columns=columns);

    #sauvegarde de tous les graphiques en proportion de leur ordonné maximum
    plt.rcParams["figure.figsize"] = figsize
    dfFree.plot.bar(stacked=True, rot = 0, title=titreFreeMax)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreFreeMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxF*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxFree.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfSFR.plot.bar(stacked=True, rot = 0, title=titreSFRMax)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreSFRMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxS*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxSFR.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfBouygues.plot.bar(stacked=True, rot = 0, title=titreBouyguesMax)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreBouyguesMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxB*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxBouygues.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfOrange.plot.bar(stacked=True, rot = 0, title=titreOrangeMax)
    plt.grid(b=True, which='major', axis='both')
    plt.title(label = titreOrangeMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxO*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxOrange.png')
    


    #sauvegarde de tout les graphiques en fonction de l'ordonné maximale de tout les graphes
    plt.rcParams["figure.figsize"] = figsize
    dfFree.plot.bar(stacked=True, rot = 0, title=titreFreeMax)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreFreeMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxFree.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfSFR.plot.bar(stacked=True, rot = 0, title=titreSFRMax)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreSFRMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxSFR.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfBouygues.plot.bar(stacked=True, rot = 0, title=titreBouyguesMax)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreBouyguesMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxBouygues.png')
    

    plt.rcParams["figure.figsize"] = figsize
    dfOrange.plot.bar(stacked=True, rot = 0, title=titreOrangeMax)
    plt.grid(b=True, which='major', axis='both')
    plt.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plt.title(label = titreOrangeMax, fontsize = tailleTitre)
    plt.ylabel(texteOrdonnee, fontsize = tailleOrdonnee)
    plt.xlabel(texteAbscisse, fontsize = tailleAbscisse)
    plt.yticks(np.arange(0, maxi*1.05, 25.0))
    plt.tight_layout()
    plt.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxOrange.png')
    

    plot_clustered_stacked([dfFree, dfSFR, dfOrange, dfBouygues],["Free Mobile", "SFR", "Orange", "Bouygues Télécom"], filename = '../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenOperateurGenMax.png', title = titreGraphCommunMax, maxi = maxi)

toutEmetteurConfondus()
emetteurGenMax()

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))