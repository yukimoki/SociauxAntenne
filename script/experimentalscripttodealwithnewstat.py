import csv

with open('tables/getPopCodePostal.csv', 'r', encoding='latin-1') as File: 
    file_reader = csv.reader(File, delimiter=';')
    next(file_reader)
    header = ["code_insee","nom","population"]
    file_carre = open('tables/newmultipopcodepostal.csv', 'w')
    csv_carre_writer = csv.writer(file_carre, delimiter=';')
    csv_carre_writer.writerow(header)
    for row in file_reader:
        if "," in row[0]:
            csv_carre_writer.writerow([row[0], row[1], row[2]])

print("ok")