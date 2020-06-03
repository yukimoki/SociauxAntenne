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
            listSup140M.add(row[0])
        elif(int(row[2])>100000):
            listInf140M.add(row[0])
        elif(int(row[2])>80000):
            listInf100M.add(row[0])
        elif(int(row[2])>60000):
            listInf80M.add(row[0])
        elif(int(row[2])>40000):
            listInf60M.add(row[0])
        elif(int(row[2])>20000):
            listInf40M.add(row[0])
        elif(int(row[2])>10000):
            listInf20M.add(row[0])
        elif(int(row[2])>5000):
            listInf10M.add(row[0])
        elif(int(row[2])>1000):
            listInf5M.add(row[0])
        elif(int(row[2])>500):
            listInf1M.add(row[0])
        else:
            listInf05M.add(row[0])


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
print(itterator)