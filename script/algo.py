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
    selected_col = ['code_insee', 'geometry']
    dept = dept[selected_col]

    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    print("Start join")

    # join = gpd.sjoin(gdf_carre, dept, how='left', op="within")
    print("Joined!")
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    print("Start plot")
    ax = dept.plot(color='White', edgecolor='k', linewidth=0.5)
    # join.plot(column='code_insee', ax=ax)
    gdf_carre.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25)
    print("Ploted!")
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))
    plt.show()
    return gdf_carre


def get_holder_point(src_point, search_dist, holder_gdf):

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

    return closest_holder, nb_holder_ok, distance


def get_holder_square(carre, search_dist, holder_gdf, ax):
    perimeter = carre.exterior
    holder_next_to = set()
    holder_closest = []

    for i in range(1, 4, 2):
        for j in range(1, 4, 2):
            x = perimeter.interpolate(i/16, normalized=True).x
            y = perimeter.interpolate(-j/16, normalized=True).y
            src_pt = Point(x, y)

            time_pt = time.time()
            r = get_holder_point(src_pt, search_dist, holder_gdf)
            print("Temps d execution point: %s secondes ---" % (time.time() - time_pt))
            holder_closest.append(r[0]['ID_SUP'].iloc[0])
            r[0].plot(ax=ax, color='red', zorder=4)

            for h in r[1]['ID_SUP']:
                holder_next_to.add(h)

            perimeter_sup = src_pt.buffer(r[2] + 0.003)
            perimeter_max = src_pt.buffer((search_dist))
            fg = GeoSeries([src_pt, perimeter_sup, perimeter_max], crs='epsg:4326')
            figure = gpd.GeoDataFrame(geometry=gpd.GeoSeries(fg, crs='epsg:4326'))
            figure.loc[[0], 'geometry'].plot(ax=ax, color='green', zorder=3)
            figure.loc[[1], 'geometry'].plot(ax=ax, color='none', edgecolor='red', linewidth=1, zorder=3)
            figure.loc[[2], 'geometry'].plot(ax=ax, color='none', edgecolor='green', linewidth=1, zorder=3)

    return holder_closest, holder_next_to


def show_holder_around(src_point, search_dist):
    carre = departs_shape()
    c = carre.loc[carre.geometry.contains(src_point.buffer(0.00005))]
    ax = carre.plot(color='none', edgecolor='k', linewidth=0.25, zorder=1)
    c.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25, zorder=2)

    holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
    geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
    holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

    r = get_holder_point(src_point, search_dist, holder_gdf)
    r[0].plot(ax=ax, color='red', zorder=4)
    print('distance of closest holder:', r[2])
    print(r[1], 'holder next to th point: lon='+str(src_point.x)+', lat='+str(src_point.y))

    perimeter_sup = src_point.buffer(r[2]+0.003)
    perimeter_max = src_point.buffer((search_dist))
    fg = GeoSeries([src_point, perimeter_sup, perimeter_max], crs='epsg:4326')
    figure = gpd.GeoDataFrame(geometry=gpd.GeoSeries(fg, crs='epsg:4326'))
    figure.loc[[0], 'geometry'].plot(ax=ax, color='green', zorder=3)
    figure.loc[[1], 'geometry'].plot(ax=ax, color='none', edgecolor='red', linewidth=1, zorder=3)
    figure.loc[[2], 'geometry'].plot(ax=ax, color='none', edgecolor='green', linewidth=1, zorder=3)

    plt.show()


# Start time exec
start_time = time.time()
time_init = time.time()
polys = []
with open('tables/carres/carres1300000.csv') as carre_file:
    csv_reader = csv.reader(carre_file, delimiter=';')
    next(csv_reader)
    for row in csv_reader:
        tmp_tab = []
        for i in range(len(row)):
            if i > 2:
                tmp_tab.append(float(row[i].replace("'", "")))

        p_coord_tab = []
        for k in range(0, 8, 2):
            p_coord_tab.append((tmp_tab[k], tmp_tab[k + 1]))

        p = Polygon(p_coord_tab)
        polys.append(p)

series_carre = GeoSeries(polys, crs='epsg:4326')

gdf_carre = gpd.GeoDataFrame(geometry=gpd.GeoSeries(series_carre, crs='epsg:4326'))
c = gdf_carre.loc[[23191], 'geometry']
# c = gdf_carre.loc[gdf_carre.geometry.contains(Point(2.207737, 48.921505).buffer(0.00000005))] # Paris: 2.207737, 48.921505 180000.csv | paumé: 5.59196, 47.6434 130000.csv
ax = gdf_carre.plot(color='none', edgecolor='k', linewidth=0.25, zorder=1)
c.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25, zorder=2)

holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

print("Temps d execution init: %s secondes ---" % (time.time() - time_init))

time_calc = time.time()
r = get_holder_square(c, 0.1, holder_gdf, ax)
print("Temps d execution calcule: %s secondes ---" % (time.time() - time_calc))

time_dept = time.time()
dept = gpd.read_file('departements-contour/departements-20180101.shp')
dept.crs = 'epsg:4326'
selected_col = ['code_insee', 'geometry']
dept = dept[selected_col]
dept.plot(ax=ax, color='White', edgecolor='k', linewidth=0.5)

print("Temps d execution dept: %s secondes ---" % (time.time() - time_dept))
print(r)
# Show execution time
print("Temps d execution total: %s secondes ---" % (time.time() - start_time))

plt.show()

# res = init_files()
# print("Nb lignes support: ", len(res[0]))
# print("Nb lignes départements: ", len(res[1]))
# print("Nb lignes carres: ", len(res[2]))
