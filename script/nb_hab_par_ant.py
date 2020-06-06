# -*-coding:UTF-8 -*
import pandas as pd
import sys
import progress
import matplotlib.pyplot as plt
import stat

# df_carres_sup = pd.read_csv('tables/finalDB/CarresDistSupProche.csv', delimiter=";")
# df_carres_socio = pd.read_csv('tables/finalDB/carres-stats-avec-nb-antennes.csv', delimiter="\t", usecols=["LAEA", "poptot"])
# df_support = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=";")
#
# df_carres = df_carres_sup.join(df_carres_socio.set_index('LAEA'), on='IDcrs')
# df_support['NbHab'] = 0
# hab_by_holder = dict()
# bar = Bar('find total nbHab for each holder', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=len(df_carres)-1)
# for idx, carre in df_carres[["IdSupProchePt1", "IdSupProchePt2", "IdSupProchePt3", "IdSupProchePt4"]].iterrows():
#     point_hab = df_carres.loc[idx, ['poptot']].values[0]/4
#     for id_sup in carre:
#         hab_by_holder[id_sup] = hab_by_holder.get(id_sup, 0) + point_hab
#     bar.next()
# bar.finish()
#
# bar = Bar('Update support dataframe with nbHab', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=len(df_support)-1)
# for idx, support in df_support.iterrows():
#     if int(support['ID_SUP']) in hab_by_holder:
#         df_support.loc[idx, ['c']] = hab_by_holder[int(support['ID_SUP'])]
#     else:
#         df_support.loc[idx, ['NbHab']] = "NaN"
#     bar.next()
# bar.finish()
#
# df_support.to_csv('tables/finalDB/nb_hab_par_ant.csv', sep=";", columns=['ID_SUP', 'NbHab'])

df_support = pd.read_csv('tables/finalDB/nb_hab_par_ant.csv', sep=";")
titre = sys.argv[1]
x_label = "Nombre d'habitant proche"
x = "NbHab"
y_label = "Nombre de support"
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
        modif = input("Modification du paramètre: \""+str(list_param[option-1])+"\" :\n")
        print("Paramètre", list_param[option-1], "modifié en", modif)
        list_param[int(option) - 1] = modif

    else:
        if option == 8:
            if list_param[6] is "on":
                df_support[x].plot.density()
            else:
                df_support['NbHab'].hist(bins=int(list_param[5]))
            plt.title(list_param[0])
            plt.xlabel(list_param[1], fontsize=14)
            plt.ylabel(list_param[3], fontsize=14)
            plt.show()
            plt.close()

        else:
            stop = True

print("Exiting...")
