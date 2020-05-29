import csv
import pandas as pd

with open('tables/carrePlusDe10/finalcarres.csv', 'r') as in_file:
    file_reader = csv.reader(in_file, delimiter=';')
    with open('tables/carrePlusDe10/CarresDistSupProche.csv', 'w') as out_file:
        file_writer = csv.writer(out_file)
        new_header = ["num", "IDsurface", "IDcrs", "x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "IdSupProchePt1", "DistSupProchePt1", "IdSupProchePt2", "DistSupProchePt2", "IdSupProchePt3", "DistSupProchePt3", "IdSupProchePt4", "DistSupProchePt4", "IdAllSupProche"]
        file_writer.writerow(new_header)
        next(file_reader)
        for read_row in file_reader:
            read_row = ";".join(read_row).replace("'", "").split(';')
            new_row = read_row[0:11]
            for i in range(4):
                tmp = read_row[11+i]
                tmp = tmp.split("-")
                new_row.append(tmp[0])
                new_row.append(tmp[1])
            new_row.append(read_row[-1])
            file_writer.writerow(new_row)

