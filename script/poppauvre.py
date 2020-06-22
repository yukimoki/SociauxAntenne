# -*-coding:UTF-8 -*
import pandas as pd
import sys

from progress.bar import Bar
import matplotlib.pyplot as plt
import stat

# df_carres_sup = pd.read_csv('tables/finalDB/CarresDistSupProche.csv', delimiter=";", usecols=["IDcrs", "IdSupProchePt1", "DistSupProchePt1", "IdSupProchePt2", "DistSupProchePt2", "IdSupProchePt3", "DistSupProchePt3", "IdSupProchePt4", "DistSupProchePt4"])
# df_carres_socio = pd.read_csv('tables/finalDB/StatsSocioCarres.csv', delimiter="\t", usecols=["LAEA", "poptot", "pcmenagespauvres"])
#
# df_carres = df_carres_sup.join(df_carres_socio.set_index('LAEA'), on='IDcrs')
# df_carres = df_carres.loc[df_carres['poptot'] > 100]
# data_dict = {}
# bar = Bar('traitement carres', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=len(df_carres)-1)
# for idx, carre in df_carres.iterrows():
#     pop_total, pc_pauvre = df_carres.loc[idx, ['poptot', 'pcmenagespauvres']].values
#     pop_pauvre = pop_total * pc_pauvre
#     stat_square = [pop_total, pop_pauvre]
#     data_dict[pop_total] = [data_dict.setdefault(pop_total, [0, 0])[i] + stat_square[i] for i in range(len(stat_square))]
#     bar.next()
# bar.finish()
# df_stat = pd.DataFrame.from_dict(data=data_dict, columns=['POP_TOTAL', 'POP_PAUVRE'], orient='index')
# print(df_stat)
# df_stat.to_csv('tables/finalDB/tmp_stat.csv', sep=";")
# ****************************************************************************

df_stat = pd.read_csv('tables/finalDB/tmp_stat.csv', sep=";", dtype='float64', header=0, names=['POP_CARRE', 'POP_TOTAL', 'POP_PAUVRE'])
df_stat.sort_values(by=['POP_CARRE'], inplace=True)
print(df_stat)

df_stat['POP_NON_PAUVRE'] = df_stat['POP_TOTAL'] - df_stat['POP_PAUVRE']

df_norm = df_stat.copy()
df_norm['POP_TOTAL'] = df_norm['POP_TOTAL'] / df_norm['POP_TOTAL'].sum()
df_norm['POP_PAUVRE'] = df_norm['POP_PAUVRE'] / df_norm['POP_PAUVRE'].sum()
df_norm['POP_NON_PAUVRE'] = df_norm['POP_NON_PAUVRE'] / df_norm['POP_NON_PAUVRE'].sum()

print(df_stat)

# df_stat.plot(kind='line', x='POP_CARRE', y='POP_PAUVRE')
# df_stat.plot(kind='line', x='POP_CARRE', y='POP_TOTAL')
limit_x = 4000
pas = 100
df_norm = df_norm[df_norm['POP_CARRE'] < limit_x]
df_stat = df_stat[df_stat['POP_CARRE'] < limit_x]

df_stat.plot.bar(x='POP_CARRE', y=['POP_NON_PAUVRE', 'POP_PAUVRE'], stacked=True, xticks=range(0, limit_x, pas))
plt.xlabel("Nombre d'habitant par carrés")
plt.ylabel("Nombre d'habitant total")
plt.title("Nombre d'habitant total des carres de n habitants (n < "+str(limit_x)+", population total étudiée: "+str(int(df_stat['POP_TOTAL'].sum()))+" hab)")

fig, (ax1, ax2) = plt.subplots(2, 1)
plt.subplots_adjust(hspace=0.3)

df_norm.plot(kind='bar', ax=ax1, x='POP_CARRE', y=['POP_TOTAL'], xticks=range(0, limit_x, pas))
ax1.xaxis.set_ticks(range(0, limit_x, pas))
ax1.xaxis.set_label_text("Nombre d'habitant par carrés")
ax1.yaxis.set_label_text("Proportion de la population total étudiée ("+str(int(df_stat['POP_TOTAL'].sum()))+" hab)")
ax1.set_title("Densité de la population en fonction du nombre d'habitant par carrés de moins de "+str(limit_x)+" habitants")

df_norm.plot(kind='bar', ax=ax2, x='POP_CARRE', y=['POP_PAUVRE'], xticks=range(0, limit_x, pas), color='orange')
ax2.xaxis.set_ticks(range(0, limit_x, pas))
ax2.xaxis.set_label_text("Nombre d'habitant par carrés")
ax2.yaxis.set_label_text("Proportion de la population pauvre étudiée ("+str(int(df_stat['POP_PAUVRE'].sum()))+" hab)")
ax2.set_title("Densité de la population pauvre en fonction du nombre d'habitant par carrés de moins de "+str(limit_x)+" habitants")

# df_norm.plot.scatter(x='POP_CARRE', y='POP_TOTAL')
# df_stat['POP_TOTAL'].plot.density()
# df_stat['POP_CARRE'].plot.hist(bins=100, alpha=0.5, by='POP_TOTAL')

plt.show()

print("Exiting...")
