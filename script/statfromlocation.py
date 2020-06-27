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

listInf100M = set() 

listInf120M =set()

listInf140M = set() 

listInf220M =set()

listInf400M =set()

listSup400M = set()


itterator = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

lea       = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]


with open('tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
    file_reader = csv.reader(File, delimiter=';')
    next(file_reader)
    for row in file_reader:
        if(int(row[2])>400000):
            temp = row[0].split("-")
            for i in temp:
                lea[13]+=1
                listSup400M.add(i)
        elif(int(row[2])>220000):
            temp = row[0].split("-")
            for i in temp:
                lea[12]+=1
                listInf400M.add(i)
        elif(int(row[2])>140000):
            temp = row[0].split("-")
            for i in temp:
                lea[11]+=1
                listInf220M.add(i)
        elif(int(row[2])>120000):
            temp = row[0].split("-")
            for i in temp:
                lea[10]+=1
                listInf140M.add(i)
        elif(int(row[2])>100000):
            temp = row[0].split("-")
            for i in temp:
                lea[9]+=1
                listInf120M.add(i)
        elif(int(row[2])>80000):
            temp = row[0].split("-")
            for i in temp:
                lea[8]+=1
                listInf100M.add(i)
        elif(int(row[2])>60000):
            temp = row[0].split("-")
            for i in temp:
                lea[7]+=1
                listInf80M.add(i)
        elif(int(row[2])>40000):
            temp = row[0].split("-")
            for i in temp:
                lea[6]+=1
                listInf60M.add(i)
        elif(int(row[2])>20000):
            temp = row[0].split("-")
            for i in temp:
                lea[5]+=1
                listInf40M.add(i)
        elif(int(row[2])>10000):
            temp = row[0].split("-")
            for i in temp:
                lea[4]+=1
                listInf20M.add(i)
        elif(int(row[2])>5000):
            temp = row[0].split("-")
            for i in temp:
                lea[3]+=1
                listInf10M.add(i)
        elif(int(row[2])>1000):
            temp = row[0].split("-")
            for i in temp:
                lea[2]+=1
                listInf5M.add(i)
        elif(int(row[2])>500):
            temp = row[0].split("-")
            for i in temp:
                lea[1]+=1
                listInf1M.add(i)
        else:
            temp = row[0].split("-")
            for i in temp:
                lea[0]+=1
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
        elif(listInf120M.__contains__(row[5].replace("'", ""))):
            itterator[9] += 1
        elif(listInf140M.__contains__(row[5].replace("'", ""))):
            itterator[10] += 1
        elif(listInf220M.__contains__(row[5].replace("'", ""))):
            itterator[11] += 1     
        elif(listInf400M.__contains__(row[5].replace("'", ""))):
            itterator[12] += 1
        elif(listSup400M.__contains__(row[5].replace("'", ""))):
            itterator[13] += 1
        else:
            print(row)

print("ok")
x=0
for j in itterator:
    x +=j
print(x)
data = {"Nombre de communes":lea,
        "Nombre de support":itterator
        };

index = ["0", "0,5", "1", "5", "10", "20", "40", "60", "80", "100","120","140","220","400"];
print('k2')
dataFrame = pd.DataFrame(data=data, index=index);

dataFrame.plot.line(rot=25, title="Nombre de support en fonction de la population de la commune");
plot.ylabel("Nombre")
plot.xlabel("Nombre d'habitants (en milliers)")
plot.tight_layout()
print("okau")
plot.savefig('tables/statpopPoint.png')
print(lea)
