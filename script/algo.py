# -*-coding: UTF-8 -*
import csv
import geopandas
import matplotlib.pyplot as plt
import tkinter
from geopandas import GeoSeries
import rtree
from shapely.geometry import Polygon, geo
import shapefile
import re
import time


def init_files():
    """
    Init file content in dictionary
    :return:
    """
    with open('tables/finalDB/SUPPORT.csv', 'r') as supports_file:
        reader_csv = csv.reader(supports_file, delimiter=';')
        supports = {}
        next(reader_csv)
        for row in reader_csv:
            supports[row[0]] = [row[1], row[2], row[5]]

    with open('tables/depart_limitrophe.txt', 'r') as departs_file:
        reader_csv = csv.reader(departs_file, delimiter=':')
        departs = {}
        for row in reader_csv:
            departs[row[0]] = row[1].split(',')

    for num_name in range(0, 2200000, 100000):
        with open('tables/carres/carres'+i+'.csv', 'r') as carres_file:
            reader_csv = csv.reader(carres_file, delimiter=';')
            carres = {}
            next(reader_csv)
            for row in reader_csv:
                carres[row[0]] = (row[3], row[4])

    return supports, departs, carres


def departs_shape():

    dept = geopandas.read_file('departements-contour/departements-20180101.shp')
    dept.crs = 'epsg:4326'

    polys = []
    for num_name in range(0, 2200000, 1000000):
        print("Extract square form carres",num_name,".csv")
        with open('tables/carres/carres'+str(num_name)+'.csv') as carre_file:
            csv_reader = csv.reader(carre_file, delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                for i in range(len(row)):
                    if i > 2:
                        row[i] = float(row[i].replace("'", ""))
    
                tmp_tab =[(row[3], row[4]), (row[5], row[6]), (row[7], row[8]), (row[9], row[10])]
                p = Polygon(tmp_tab)
                polys.append(p)

        series_carre = GeoSeries(polys, crs='epsg:4326')

    gdf_carre = geopandas.GeoDataFrame(geometry=geopandas.GeoSeries(series_carre, crs='epsg:4326'))
    selected_col = ['code_insee', 'geometry']
    dept = dept[selected_col]

    print("Start join")
    join = geopandas.sjoin(gdf_carre, dept, how='left', op="within")
    print("Joined!")
    ax = dept.plot(color='White', edgecolor='k', linewidth=0.5)
    join.plot(column='code_insee', ax=ax)

    plt.show()


# Start time exec
start_time = time.time()

departs_shape()

# Show execution time
print("Temps d execution : %s secondes ---" % (time.time() - start_time))

    # departs = {}
    # for dept in range(len(sf)):
    #     if re.search('[A-Z]', rec[dept].record[0]):
    #         departs[rec[dept].record[0]] = rec[dept].shape.points
    #     elif int(rec[dept].record[0]) < 900:
    #         pop = 1
    #         departs[rec[dept].record[0]] = rec[dept].shape.points


# res = init_files()
# print("Nb lignes support: ", len(res[0]))
# print("Nb lignes départements: ", len(res[1]))
# print("Nb lignes carres: ", len(res[2]))

