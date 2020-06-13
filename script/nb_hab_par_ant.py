# -*-coding:UTF-8 -*
import pandas as pd
import sys
from progress.bar import Bar
import matplotlib.pyplot as plt
import stat

df_carres_sup = pd.read_csv('tables/finalDB/CarresDistSupProche.csv', delimiter=";", usecols=["IDcrs", "IdSupProchePt1", "DistSupProchePt1", "IdSupProchePt2", "DistSupProchePt2", "IdSupProchePt3", "DistSupProchePt3", "IdSupProchePt4", "DistSupProchePt4"])
df_carres_socio = pd.read_csv('tables/finalDB/StatsSocioCarres.csv', delimiter="\t", usecols=["LAEA", "poptot", "pcmenagespauvres"])

df_carres = df_carres_sup.join(df_carres_socio.set_index('LAEA'), on='IDcrs')
df_carres = df_carres.loc[df_carres['poptot'] > 100]
hab_by_holder = dict()
bar = Bar('find total nbHab for each holder', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=len(df_carres)-1)
for idx, carre in df_carres[["IdSupProchePt1", "IdSupProchePt2", "IdSupProchePt3", "IdSupProchePt4"]].iterrows():
    pop_total, pc_pauvre = df_carres.loc[idx, ['poptot', 'pcmenagespauvres']].values
    pop_total /= 4
    pop_pauvre = pop_total * pc_pauvre
    pop_nonpauvre = pop_total - pop_pauvre
    stat_for_pt = [pop_total, pop_pauvre, pop_nonpauvre]
    for id_sup in carre:
        hab_by_holder[id_sup] = [hab_by_holder.setdefault(id_sup, [0, 0, 0])[i] + stat_for_pt[i] for i in range(len(stat_for_pt))]
    bar.next()
bar.finish()

df_stat = pd.DataFrame.from_dict(data=hab_by_holder, columns=['POP_TOTAL', 'POP_PAUVRE', 'POP_NON_PAUVRE'], orient='index')
print(df_stat)
df_stat.to_csv('tables/finalDB/nb_hab_par_ant.csv', sep=";")
# ****************************************************************************

df_stat = pd.read_csv('tables/finalDB/nb_hab_par_ant.csv', index_col=0, sep=";", dtype='float64')
print(df_stat)
titre = sys.argv[1]
x_label = "Nombre d'habitant proche"
x = 'POP_TOTAL'
y_label = "Fréquence"
y = ""
bins = 300
list_param = [titre, x_label, x, y_label, y, bins, "off"]
stop = False
while not stop:
    print("1. Titre :", list_param[0])
    print("2. x label:", list_param[1])
    print("3. x :", list_param[2])
    print("4. y label:", list_param[3])
    print("5. y :", list_param[4])
    print("6. Echantillonage:", list_param[5])
    print("7. Densité: ", list_param[6])
    print("8. Afficher le graphique")
    print("9. Exit")
    print("**************************************")
    option = int(input("Tapez un numéro pour choisir :\n"))

    if option in range(1, 8):
        print("+++++++++++++++++++++++++++++++++++++++")
        print("Modification du paramètre: \""+str(list_param[option-1])+"\" :\n")
        if option in [3, 5]:
            i=1
            print("0. ALL")
            for col in list(df_stat.columns):
                print(str(i)+".", col)
                i += 1
            idx = int(input("Tapez un numéro pour choisir :\n"))
            if idx != 0:
                modif = df_stat.columns[idx-1]
            else:
                modif = list(df_stat.columns)
        else:
            modif = input("Nouvelle valeur:\n")
        print("Paramètre", list_param[option-1], "modifié en", modif)
        list_param[int(option) - 1] = modif

    else:
        if option == 8:
            if list_param[6] == "on":
                df_stat[list_param[2]].plot.density()
            else:
                # df_stat['POP_NON_PAUVRE'].plot.hist(bins=int(list_param[5]), alpha=0.5)#
                # df_stat['POP_PAUVRE'].plot.hist(bins=int(list_param[5]), alpha=0.5)
                df_stat.hist(bins=int(list_param[5]), column=list_param[2])
            plt.title(list_param[0]+"\nCritère étudié: "+str(list_param[2]), fontsize=20)
            plt.xlabel(list_param[1], fontsize=16)
            plt.ylabel(list_param[3], fontsize=16)
            plt.xlim(0, 1000)
            plt.xticks(range(0, 1000, 50))
            plt.grid(True)
            if len(list_param[2]) > 1:
                list_param[2] = ['POP_TOTAL']
            plt.text(10, 10, "Population total étudiée: "+f"{int(df_stat[list_param[2]].sum()):,}".replace(',', ' '))
            plt.show()
            plt.close()

        else:
            stop = True

print("Exiting...")
