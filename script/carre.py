# -*-coding:UTF-8 -*
import csv
import os

list_id = set()


with open('tables/carres-stats-avec-nb-antennes', 'r', encoding='latin-1') as File:
    file_reader = csv.reader(File, delimiter='\t')
    next(file_reader)
    for row in file_reader:
        list_id.add(row[0])

#faut rajouter un dir /tables/carrePlusDe10


header = ["'num'", "'IDsurface'","'IDcrs'","'x1'","'y1'","'x2'","'y2'","'x3'","'y3'","'x4'","'y4'"]

for num_name in range( 0, 2200001, 100000):
        print("Extract square form carres", num_name, ".csv")
        with open('tables/carres/carres' + str(num_name) + '.csv') as carre_file:
            csv_reader = csv.reader(carre_file, delimiter=';')
            next(csv_reader)
            file_carre = open('tables/carrePlusDe10/carres' + str(num_name) + '.csv', 'w')
            csv_carre_writer = csv.writer(file_carre, delimiter=';')
            csv_carre_writer.writerow(header)
            for row in csv_reader:
                if(list_id.__contains__(row[2].replace("'", ""))):
                    csv_carre_writer.writerow(row)
            file_carre.close()

