import csv
import pandas as pd
import matplotlib.pyplot as plot



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

itterator = [0,0,0,0,0,0,0,0,0,0,0]

with open('tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
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


with open('tables/finalDB/SUPPORT.csv', 'r', encoding='latin-1') as FileSup: 
    file_readerSup = csv.reader(FileSup, delimiter=';')
    next(file_readerSup)
    for row in file_readerSup:
        if(listInf05M.__contains__(row[5].replace("'", ""))):
            itterator[0] += 1
        elif(listInf1M.__contains__(row[5].replace("'", ""))):
            itterator[1] += 1
        elif(listInf5M.__contains__(row[5].replace("'", ""))):
            itterator[2] += 1
        elif(listInf10M.__contains__(row[5].replace("'", ""))):
            itterator[3] += 1
        elif(listInf20M.__contains__(row[5].replace("'", ""))):
            itterator[4] += 1
        elif(listInf40M.__contains__(row[5].replace("'", ""))):
            itterator[5] += 1
        elif(listInf60M.__contains__(row[5].replace("'", ""))):
            itterator[6] += 1
        elif(listInf80M.__contains__(row[5].replace("'", ""))):
            itterator[7] += 1
        elif(listInf100M.__contains__(row[5].replace("'", ""))):
            itterator[8] += 1
        elif(listInf140M.__contains__(row[5].replace("'", ""))):
            itterator[9] += 1
        elif(listSup140M.__contains__(row[5].replace("'", ""))):
            itterator[10] += 1
        else:
            print(row)

print("ok")
x=0
for j in itterator:
    x +=j
print(x)


data = {"range":["0 to 0.5", "0.5 to 1", "1M to 5", "5 to 10", "10 to 20", "20 to 40", "40 to 60", "60 to 80", "80 to 100", "100 to 140", "plus de 140"],
        "values":itterator
        };

dataFrame = pd.DataFrame(data=data);

dataFrame.plot.bar(x="range", y="values", rot=25, title="Nombre de support en fonction de la population de la commune(en millier d'hab)");
print("okau")
plot.savefig('tables/statpop.png')