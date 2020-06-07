import csv
import pandas as pd
import matplotlib.pyplot as plot
import numpy as np
import math
import sys
import time
import os

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


#fonction qui génère un graph avec plusieur bar entassé
def plot_clustered_stacked(dfall, labels=None, filename="stat.png", title="Nombre d'émetteurs par génération, population et opérateur",  H="/", **kwargs):

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plot.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 25)
    axe.set_title(title)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plot.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)

    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig(filename)


#dictionnaire qui contient toutes les stations et un tableau de booléen pour chaque génération d'emetteur 
d = {}

with open('../tables/finalDB/EMETTEUR.csv', 'r', encoding='latin-1') as FileEme:
    file_readerEme = csv.reader(FileEme, delimiter=';')
    next(file_readerEme)
    
    #represente pour chaque support les générations des emetteur présent et les fournissuers qui les proposent
    #l'ordre est le suivant 2G, 3G, 4G, 5G pour Free puis pour SFR, Orange et Bouygues
    tabGenFournisseur = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

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
            tabGenFournisseur[i*4] = True
        elif("UMTS" in emetteur[3]):
            tabGenFournisseur[i*4+1] = True
        elif("LTE" in emetteur[3]):
            tabGenFournisseur[i*4+2] = True
        elif("NG" in emetteur[3]):
            tabGenFournisseur[i*4+3] = True

        if(numSup in d):
            
            oldtabGenFournisseur = d[numSup]
            for i in range(16):
                if(tabGenFournisseur[i]==True or oldtabGenFournisseur[i]==True):
                    tabGenFournisseur[i] = True
        
        d[numSup] = tabGenFournisseur
        tabGenFournisseur = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

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

    gen2GFree = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GFree = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GFree = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GFree = [0,0,0,0,0,0,0,0,0,0,0]

    gen2GSFR = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GSFR = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GSFR = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GSFR = [0,0,0,0,0,0,0,0,0,0,0]

    gen2GBouygues = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GBouygues = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GBouygues = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GBouygues = [0,0,0,0,0,0,0,0,0,0,0]

    gen2GOrange = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GOrange = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GOrange = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GOrange = [0,0,0,0,0,0,0,0,0,0,0]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        #pour chaque support
        for support in file_readerSup:

            #on regarde si le support est présent dans le dictionnaire
            if(support[0] in d):
                tabGenFournisseur = d[support[0]]
                
                #on regarde si le support à moins de 0.5 mille habitants
                if(listInf05M.__contains__(support[5].replace("'", ""))):

                    #on Comptabilise chaque generation d'emetteur pour Free
                    if(tabGenFournisseur[3]):
                        gen5GFree[0]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[0]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[0]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[0]+=1

                    #on comptabilise chaque generation d'emetteur pour SFR
                    if(tabGenFournisseur[7]):
                        gen5GSFR[0]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[0]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[0]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[0]+=1

                    #on comptabilise chaque generation d'emetteur pour Orange
                    if(tabGenFournisseur[11]):
                        gen5GOrange[0]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[0]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[0]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[0]+=1

                    #on comptabilise chaque generation d'emetteur pour Bouygues
                    if(tabGenFournisseur[15]):
                        gen5GBouygues[0]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[0]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[0]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[0]+=1

                #si le support à plus d'habitants qui lui sont liés on comptabilise de la même manière
                elif(listInf1M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[1]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[1]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[1]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[1]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[1]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[1]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[1]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[1]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[1]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[1]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[1]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[1]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[1]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[1]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[1]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[1]+=1

                elif(listInf5M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[2]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[2]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[2]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[2]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[2]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[2]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[2]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[2]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[2]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[2]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[2]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[2]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[2]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[2]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[2]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[2]+=1

                elif(listInf10M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[3]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[3]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[3]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[3]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[3]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[3]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[3]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[3]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[3]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[3]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[3]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[3]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[3]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[3]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[3]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[3]+=1

                elif(listInf20M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[4]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[4]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[4]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[4]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[4]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[4]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[4]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[4]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[4]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[4]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[4]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[4]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[4]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[4]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[4]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[4]+=1

                elif(listInf40M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[5]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[5]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[5]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[5]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[5]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[5]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[5]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[5]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[5]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[5]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[5]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[5]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[5]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[5]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[5]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[5]+=1

                elif(listInf60M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[6]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[6]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[6]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[6]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[6]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[6]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[6]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[6]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[6]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[6]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[6]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[6]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[6]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[6]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[6]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[6]+=1

                elif(listInf80M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[7]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[7]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[7]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[7]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[7]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[7]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[7]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[7]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[7]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[7]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[7]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[7]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[7]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[7]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[7]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[7]+=1

                elif(listInf100M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[8]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[8]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[8]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[8]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[8]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[8]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[8]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[8]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[8]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[8]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[8]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[8]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[8]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[8]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[8]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[8]+=1

                elif(listInf140M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[9]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[9]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[9]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[9]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[9]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[9]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[9]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[9]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[9]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[9]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[9]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[9]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[9]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[9]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[9]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[9]+=1

                elif(listSup140M.__contains__(support[5].replace("'", ""))):
       
                    if(tabGenFournisseur[3]):
                        gen5GFree[10]+=1

                    if(tabGenFournisseur[2]):
                        gen4GFree[10]+=1

                    if(tabGenFournisseur[1]):
                        gen3GFree[10]+=1

                    if(tabGenFournisseur[0]):
                        gen2GFree[10]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[10]+=1

                    if(tabGenFournisseur[6]):
                        gen4GSFR[10]+=1

                    if(tabGenFournisseur[5]):
                        gen3GSFR[10]+=1

                    if(tabGenFournisseur[4]):
                        gen2GSFR[10]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[10]+=1

                    if(tabGenFournisseur[10]):
                        gen4GOrange[10]+=1

                    if(tabGenFournisseur[9]):
                        gen3GOrange[10]+=1

                    if(tabGenFournisseur[8]):
                        gen2GOrange[10]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[10]+=1

                    if(tabGenFournisseur[14]):
                        gen4GBouygues[10]+=1

                    if(tabGenFournisseur[13]):
                        gen3GBouygues[10]+=1

                    if(tabGenFournisseur[12]):
                        gen2GBouygues[10]+=1


    dataFree = {
            "2G":gen2GFree,
            "3G":gen3GFree,
            "4G":gen4GFree,
            "5G":gen5GFree
            };

    dataSFR = {
            "2G":gen2GSFR,
            "3G":gen3GSFR,
            "4G":gen4GSFR,
            "5G":gen5GSFR
            };

    dataOrange = {
            "2G":gen2GOrange,
            "3G":gen3GOrange,
            "4G":gen4GOrange,
            "5G":gen5GOrange
            };

    dataBouygues = {
            "2G":gen2GBouygues,
            "3G":gen3GBouygues,
            "4G":gen4GBouygues,
            "5G":gen5GBouygues
            };

    index = ["0-0.5", "0.5-1", "1-5", "5-10", "10-20", "20-40", "40-60", "60-80", "80-100", "100-140", ">140"]
    columns = ["2G", "3G", "4G", "5G"]

    tabNbEmeFree = [0,0,0,0,0,0,0,0,0,0,0]
    tabNbEmeOrange = [0,0,0,0,0,0,0,0,0,0,0]
    tabNbEmeSFR = [0,0,0,0,0,0,0,0,0,0,0]
    tabNbEmeBouygues = [0,0,0,0,0,0,0,0,0,0,0]

    for i in range(len(gen2GFree)):
        tabNbEmeFree[i]= gen2GFree[i] + gen3GFree[i] + gen4GFree[i] + gen5GFree[i]
        tabNbEmeOrange[i]= gen2GOrange[i] + gen3GOrange[i] + gen4GOrange[i] + gen5GOrange[i]
        tabNbEmeSFR[i]= gen2GSFR[i] + gen3GSFR[i] + gen4GSFR[i] + gen5GSFR[i]
        tabNbEmeBouygues[i]= gen2GBouygues[i] + gen3GBouygues[i] + gen4GBouygues[i] + gen5GBouygues[i]

    maxB = max(tabNbEmeBouygues)
    maxF = max(tabNbEmeFree)
    maxS = max(tabNbEmeSFR)
    maxO = max(tabNbEmeOrange)

    maxi = max([maxB, maxF, maxS, maxO])

    dfFree = pd.DataFrame(data=dataFree, index=index, columns=columns);
    dfSFR = pd.DataFrame(data=dataSFR, index=index, columns=columns);
    dfOrange = pd.DataFrame(data=dataOrange, index=index, columns=columns);
    dfBouygues = pd.DataFrame(data=dataBouygues, index=index, columns=columns);

    #sauvegarde de tous les graphiques en proportion de leur ordonné maximum
    dfFree.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population de Free Mobile")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousFree.png')
    plot.clf()


    dfSFR.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population de SFR")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousSFR.png')
    plot.clf()


    dfBouygues.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population de Bouygues Telecom")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousBouygues.png')
    plot.clf()


    dfOrange.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population d'Orange")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenTousOrange.png')
    plot.clf()


    #sauvegarde de tout les graphiques en fonction de l'ordonné maximale de tout les graphes
    dfFree.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population de Free Mobile")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousFree.png')
    plot.clf()


    dfSFR.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population de SFR")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousSFR.png')
    plot.clf()


    dfBouygues.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population de Bouygues Telecom")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousBouygues.png')
    plot.clf()


    dfOrange.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération et population d'Orange")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenTousOrange.png')
    plot.clf()

    plot_clustered_stacked([dfFree, dfSFR, dfOrange, dfBouygues],["Free Mobile", "SFR", "Orange", "Bouygues Telecom"], '../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenOperateurTous.png')


def emetteurGenMax():

    gen2GFree = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GFree = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GFree = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GFree = [0,0,0,0,0,0,0,0,0,0,0]

    gen2GSFR = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GSFR = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GSFR = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GSFR = [0,0,0,0,0,0,0,0,0,0,0]

    gen2GBouygues = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GBouygues = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GBouygues = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GBouygues = [0,0,0,0,0,0,0,0,0,0,0]

    gen2GOrange = [0,0,0,0,0,0,0,0,0,0,0]
    gen3GOrange = [0,0,0,0,0,0,0,0,0,0,0]
    gen4GOrange = [0,0,0,0,0,0,0,0,0,0,0]
    gen5GOrange = [0,0,0,0,0,0,0,0,0,0,0]

    with open('../tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
        file_readerSup = csv.reader(FileSup, delimiter=';')
        next(file_readerSup)
        #pour chaque support
        for support in file_readerSup:

            #on regarde si le support est présent dans le dictionnaire
            if(support[0] in d):
                tabGenFournisseur = d[support[0]]
                
                #on regarde si le support à moins de 0.5 mille habitants
                if(listInf05M.__contains__(support[5].replace("'", ""))):

                    #on Comptabilise chaque generation d'emetteur pour Free
                    if(tabGenFournisseur[3]):
                        gen5GFree[0]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[0]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[0]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[0]+=1

                    #on comptabilise chaque generation d'emetteur pour SFR
                    if(tabGenFournisseur[7]):
                        gen5GSFR[0]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[0]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[0]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[0]+=1

                    #on comptabilise chaque generation d'emetteur pour Orange
                    if(tabGenFournisseur[11]):
                        gen5GOrange[0]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[0]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[0]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[0]+=1

                    #on comptabilise chaque generation d'emetteur pour Bouygues
                    if(tabGenFournisseur[15]):
                        gen5GBouygues[0]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[0]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[0]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[0]+=1

                #si le support à plus d'habitants qui lui sont liés on comptabilise de la même manière
                elif(listInf1M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[1]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[1]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[1]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[1]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[1]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[1]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[1]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[1]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[1]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[1]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[1]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[1]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[1]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[1]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[1]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[1]+=1

                elif(listInf5M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[2]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[2]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[2]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[2]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[2]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[2]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[2]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[2]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[2]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[2]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[2]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[2]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[2]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[2]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[2]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[2]+=1

                elif(listInf10M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[3]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[3]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[3]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[3]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[3]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[3]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[3]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[3]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[3]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[3]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[3]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[3]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[3]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[3]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[3]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[3]+=1

                elif(listInf20M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[4]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[4]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[4]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[4]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[4]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[4]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[4]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[4]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[4]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[4]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[4]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[4]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[4]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[4]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[4]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[4]+=1

                elif(listInf40M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[5]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[5]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[5]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[5]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[5]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[5]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[5]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[5]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[5]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[5]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[5]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[5]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[5]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[5]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[5]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[5]+=1

                elif(listInf60M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[6]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[6]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[6]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[6]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[6]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[6]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[6]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[6]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[6]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[6]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[6]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[6]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[6]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[6]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[6]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[6]+=1

                elif(listInf80M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[7]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[7]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[7]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[7]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[7]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[7]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[7]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[7]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[7]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[7]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[7]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[7]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[7]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[7]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[7]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[7]+=1

                elif(listInf100M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[8]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[8]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[8]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[8]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[8]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[8]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[8]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[8]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[8]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[8]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[8]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[8]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[8]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[8]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[8]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[8]+=1

                elif(listInf140M.__contains__(support[5].replace("'", ""))):

                    if(tabGenFournisseur[3]):
                        gen5GFree[9]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[9]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[9]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[9]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[9]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[9]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[9]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[9]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[9]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[9]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[9]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[9]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[9]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[9]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[9]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[9]+=1

                elif(listSup140M.__contains__(support[5].replace("'", ""))):
       
                    if(tabGenFournisseur[3]):
                        gen5GFree[10]+=1

                    elif(tabGenFournisseur[2]):
                        gen4GFree[10]+=1

                    elif(tabGenFournisseur[1]):
                        gen3GFree[10]+=1

                    elif(tabGenFournisseur[0]):
                        gen2GFree[10]+=1

                    
                    if(tabGenFournisseur[7]):
                        gen5GSFR[10]+=1

                    elif(tabGenFournisseur[6]):
                        gen4GSFR[10]+=1

                    elif(tabGenFournisseur[5]):
                        gen3GSFR[10]+=1

                    elif(tabGenFournisseur[4]):
                        gen2GSFR[10]+=1


                    if(tabGenFournisseur[11]):
                        gen5GOrange[10]+=1

                    elif(tabGenFournisseur[10]):
                        gen4GOrange[10]+=1

                    elif(tabGenFournisseur[9]):
                        gen3GOrange[10]+=1

                    elif(tabGenFournisseur[8]):
                        gen2GOrange[10]+=1


                    if(tabGenFournisseur[15]):
                        gen5GBouygues[10]+=1

                    elif(tabGenFournisseur[14]):
                        gen4GBouygues[10]+=1

                    elif(tabGenFournisseur[13]):
                        gen3GBouygues[10]+=1

                    elif(tabGenFournisseur[12]):
                        gen2GBouygues[10]+=1


    dataFree = {
            "2G":gen2GFree,
            "3G":gen3GFree,
            "4G":gen4GFree,
            "5G":gen5GFree
            };

    dataSFR = {
            "2G":gen2GSFR,
            "3G":gen3GSFR,
            "4G":gen4GSFR,
            "5G":gen5GSFR
            };

    dataOrange = {
            "2G":gen2GOrange,
            "3G":gen3GOrange,
            "4G":gen4GOrange,
            "5G":gen5GOrange
            };

    dataBouygues = {
            "2G":gen2GBouygues,
            "3G":gen3GBouygues,
            "4G":gen4GBouygues,
            "5G":gen5GBouygues
            };

    index = ["0-0.5", "0.5-1", "1-5", "5-10", "10-20", "20-40", "40-60", "60-80", "80-100", "100-140", ">140"]
    columns = ["2G", "3G", "4G", "5G"]

    tabNbEmeFree = [0,0,0,0,0,0,0,0,0,0,0]
    tabNbEmeOrange = [0,0,0,0,0,0,0,0,0,0,0]
    tabNbEmeSFR = [0,0,0,0,0,0,0,0,0,0,0]
    tabNbEmeBouygues = [0,0,0,0,0,0,0,0,0,0,0]

    for i in range(len(gen2GFree)):
        tabNbEmeFree[i]= gen2GFree[i] + gen3GFree[i] + gen4GFree[i] + gen5GFree[i]
        tabNbEmeOrange[i]= gen2GOrange[i] + gen3GOrange[i] + gen4GOrange[i] + gen5GOrange[i]
        tabNbEmeSFR[i]= gen2GSFR[i] + gen3GSFR[i] + gen4GSFR[i] + gen5GSFR[i]
        tabNbEmeBouygues[i]= gen2GBouygues[i] + gen3GBouygues[i] + gen4GBouygues[i] + gen5GBouygues[i]

    maxB = max(tabNbEmeBouygues)
    maxF = max(tabNbEmeFree)
    maxS = max(tabNbEmeSFR)
    maxO = max(tabNbEmeOrange)

    maxi = max([maxB, maxF, maxS, maxO])

    dfFree = pd.DataFrame(data=dataFree, index=index, columns=columns);
    dfSFR = pd.DataFrame(data=dataSFR, index=index, columns=columns);
    dfOrange = pd.DataFrame(data=dataOrange, index=index, columns=columns);
    dfBouygues = pd.DataFrame(data=dataBouygues, index=index, columns=columns);

    #sauvegarde de tous les graphiques en proportion de leur ordonné maximum
    dfFree.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population de Free Mobile")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxFree.png')
    plot.clf()


    dfSFR.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population de SFR")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxSFR.png')
    plot.clf()


    dfBouygues.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population de Bouygues Telecom")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxBouygues.png')
    plot.clf()


    dfOrange.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population d'Orange")
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateur/statPopGenMaxOrange.png')
    plot.clf()


    #sauvegarde de tout les graphiques en fonction de l'ordonné maximale de tout les graphes
    dfFree.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population de Free Mobile")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxFree.png')
    plot.clf()


    dfSFR.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population de SFR")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxSFR.png')
    plot.clf()


    dfBouygues.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population de Bouygues Telecom")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxBouygues.png')
    plot.clf()


    dfOrange.plot.bar(stacked=True, rot=25, title="Nombre d'émetteurs par génération max/support et population d'Orange")
    plot.ylim([0, math.ceil(maxi+0.1*(maxi-0))])
    plot.ylabel("Nombre de supports")
    plot.xlabel("Nombre d'habitants (en milliers)")
    plot.tight_layout()
    plot.savefig('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenMaxOrange.png')
    plot.clf()

    plot_clustered_stacked([dfFree, dfSFR, dfOrange, dfBouygues],["Free Mobile", "SFR", "Orange", "Bouygues Telecom"], '../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne/statPopGenOperateurGenMax.png', "Nombre d'émetteurs par génération max/support, population et operateur")

toutEmetteurConfondus()
emetteurGenMax()

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))