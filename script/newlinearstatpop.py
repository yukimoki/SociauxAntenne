import csv
import pandas as pd
import matplotlib.pyplot as plot


name = {}
ville = {}
tab = {}
division = {}
with open('tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
    file_reader = csv.reader(File, delimiter=';')
    next(file_reader)
    for row in file_reader:
        temp = row[0].split(",")
        for i in temp:
            name[i] = row[1]
            if(i in ville):
                ville[i] = (int(ville[i])+int(row[2]))/2
            else:
                ville[i] = row[2]
            if(i in division):
                division[i] += 1
            else:
                division[i] = 1
 
with open('tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)
    for row in file_readerSup:
        if(row[5].replace("'", "") in ville):
            if(row[5].replace("'", "") in tab):
                tab[row[5].replace("'", "")] += 1
            else:
                tab[row[5].replace("'", "")] = 1

            
print("ok")
label = []
titi = []
tooa = []
for y, item in tab.items():
    titi.append(int(ville[y]))
    tooa.append(int(item)/int(division[y]))
    if(int(item)/int(division[y])>60)|(int(ville[y])>190000):
        if((int(y)%100)>0):
            label.append(name[y]+str(int(y)%1000))
        else:
            label.append(name[y])
        print(name[y],y, " :",int(item)/int(division[y]), "supports pour ", str(ville[y]), "habitants")
    else:
        label.append("")

data = {"numpop":titi,
        "support":tooa,
        "label":label
        };


dataFrame = pd.DataFrame(data=data);

ax = dataFrame.plot(kind='scatter', x='numpop', y='support', color='red', title="Nombre de support en fonction de la population de la commune");
plot.ylabel("Nombre de support")
plot.xlabel("Nombre d'habitants")
plot.tight_layout()
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))

label_point(dataFrame.numpop, dataFrame.support, dataFrame.label, ax)

print("okau")
plot.savefig('tables/newstatpop.png')
print("fin")

plot.show()

