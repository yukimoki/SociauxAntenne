# -*-coding: UTF-8 -*
import csv
import geopandas as gpd
import pandas as pd
from descartes import PolygonPatch
from geopandas import GeoSeries, GeoDataFrame
import matplotlib.pyplot as plt
import rtree
from shapely.geometry import Polygon, Point
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
        with open('tables/carres/carres' + str(num_name) + '.csv', 'r') as carres_file:
            reader_csv = csv.reader(carres_file, delimiter=';')
            carres = {}
            next(reader_csv)
            for row in reader_csv:
                carres[row[0]] = (row[3], row[4])

    return supports, departs, carres


def departs_shape():
    dept = gpd.read_file('departements-contour/departements-20180101.shp')
    dept.crs = 'epsg:4326'

    polys = []
    # un zero de plus pour moins de données
    for num_name in range(1800000, 1800500, 1000000):
        print("Extract square form carres", num_name, ".csv")
        with open('tables/carres/carres' + str(num_name) + '.csv') as carre_file:
            csv_reader = csv.reader(carre_file, delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                tmp_tab = []
                for i in range(len(row)):
                    if i > 2:
                        tmp_tab.append(float(row[i].replace("'", "")))

                p_coord_tab = []
                for k in range(0, 8, 2):
                    p_coord_tab.append((tmp_tab[k], tmp_tab[k+1]))

                p = Polygon(p_coord_tab)
                polys.append(p)

    series_carre = GeoSeries(polys, crs='epsg:4326')

    gdf_carre = gpd.GeoDataFrame(geometry=gpd.GeoSeries(series_carre, crs='epsg:4326'))
    # selected_col = ['code_insee', 'geometry']
    # dept = dept[selected_col]

    # print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    # print("Start join")
    #
    # # join = gpd.sjoin(gdf_carre, dept, how='left', op="within")
    # print("Joined!")
    # print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    # print("Start plot")
    # ax = dept.plot(color='White', edgecolor='k', linewidth=0.5)
    # # join.plot(column='code_insee', ax=ax)
    # gdf_carre.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25)
    # print("Ploted!")
    # print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    # plt.show()
    return gdf_carre


def get_holder_around(lon, lat, search_dist, holder_gdf):

    src_point = Point(lon, lat)

    all_holder = holder_gdf.loc[holder_gdf.intersects(src_point.buffer(search_dist))]
    unary = all_holder.unary_union
    closest_holder_point = None
    distance = search_dist + 99999

    for holder_point in enumerate(unary):
        d = holder_point[1].distance(src_point)

        if d < distance:
            distance = d
            closest_holder_point = holder_point

    closest_holder = holder_gdf.loc[holder_gdf.intersects(closest_holder_point[1].buffer(0.00000005))]

    nb_holder_ok = all_holder.loc[all_holder.intersects(src_point.buffer(distance+0.003))]

    return closest_holder, len(nb_holder_ok), distance


def show_holder_around(lon, lat, search_dist):
    carre = departs_shape()
    c = carre.loc[carre.geometry.contains(Point(lon, lat).buffer(0.00005))]
    ax = carre.plot(color='none', edgecolor='k', linewidth=0.25, zorder=1)
    c.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25, zorder=2)

    holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
    geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
    holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

    r = get_holder_around(lon, lat, search_dist, holder_gdf)
    r[0].plot(ax=ax, color='red', zorder=4)
    print('distance of closest holder:', r[2])
    print(r[1], 'holder next to th point: lon='+str(lon)+', lat='+str(lat))

    src = Point(lon, lat)
    perimeter_sup = src.buffer(r[2]+0.003)
    perimeter_max = src.buffer((search_dist))
    fg = GeoSeries([src, perimeter_sup, perimeter_max], crs='epsg:4326')
    figure = gpd.GeoDataFrame(geometry=gpd.GeoSeries(fg, crs='epsg:4326'))
    figure.loc[[0], 'geometry'].plot(ax=ax, color='white', zorder=3)
    figure.loc[[1], 'geometry'].plot(ax=ax, color='none', edgecolor='red', linewidth=1, zorder=3)
    figure.loc[[2], 'geometry'].plot(ax=ax, color='none', edgecolor='green', linewidth=1, zorder=3)

    plt.show()


# Start time exec
start_time = time.time()

show_holder_around(2.207737, 48.921505, 8)

# Show execution time
print("Temps d execution total: %s secondes ---" % (time.time() - start_time))

# res = init_files()
# print("Nb lignes support: ", len(res[0]))
# print("Nb lignes départements: ", len(res[1]))
# print("Nb lignes carres: ", len(res[2]))
