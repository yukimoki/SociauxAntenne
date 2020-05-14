# -*-coding: UTF-8 -*
import csv
import geopandas
import shapefile
import re

def init_files():
    """
    Init file content in dictionary
    :return:
    """
    with open('../generateTables/tables/finalDB/SUPPORT.csv', 'r') as supports_file:
        reader_csv = csv.reader(supports_file, delimiter=';')
        supports = {}
        next(reader_csv)
        for row in reader_csv:
            supports[row[0]] = [row[1], row[2], row[5]]

    with open('depart_limitrophe.txt', 'r') as departs_file:
        reader_csv = csv.reader(departs_file, delimiter=':')
        departs = {}
        for row in reader_csv:
            departs[row[0]] = row[1].split(',')

    with open('carres/carres0.csv', 'r') as carres_file:
        reader_csv = csv.reader(carres_file, delimiter=';')
        carres = {}
        next(reader_csv)
        for row in reader_csv:
            carres[row[0]] = (row[3], row[4])

    return supports, departs, carres


def departs_shape():

    sf = shapefile.Reader("/home/nicolas/Documents/StageSocioMobile/departements-contour/departements-20180101.shp")
    rec = sf.shapeRecords()
    departs = {}
    for dept in range(len(sf)):
        if re.search('[A-Z]', rec[dept].record[0]):
            departs[rec[dept].record[0]] = rec[dept].shape.points
        elif int(rec[dept].record[0]) < 900:
            pop = 1
            departs[rec[dept].record[0]] = rec[dept].shape.points

    return departs



# res = init_files()
# print("Nb lignes support: ", len(res[0]))
# print("Nb lignes départements: ", len(res[1]))
# print("Nb lignes carres: ", len(res[2]))
departs_shape()
