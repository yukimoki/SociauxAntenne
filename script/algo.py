# -*-coding: UTF-8 -*
import csv
from typing import List, Any

import geopandas as gpd
import pandas as pd
from descartes import PolygonPatch
from geopandas import GeoSeries, GeoDataFrame
import matplotlib.pyplot as plt
import rtree
from shapely.geometry import Polygon, Point, LineString
import re
import time
from progress.bar import Bar

def init_files():
    """
    Init file content in dictionary
    (obsolete)
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
    """
    Link items of carresXXXX.csv with their postal code
    (obsolete)
    :return:
    """
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


def carresfile_to_dataframe(file_path, crs='epsg:4326'):

    df = pd.read_csv(file_path, sep=';')
    carre_coord = []
    with open(file_path) as carre_file:
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
            carre_coord.append(p)

    series_carre = GeoSeries(carre_coord, crs=crs)

    gdf_carre = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries(series_carre, crs=crs))

    return gdf_carre


def get_holder_point(src_point, search_dist, holder_gdf, crs='epsg:4326'):
    """
    Find the nearest holder from a specific point,
    then find all the holder present in a field nearly 300 meters further than the nearest support
    :param src_point: point of reference to find near holders : (Point(lat,lon))
    :param search_dist: maximum radius for search in degrees : (float) | 1 degree ~= 111km for lat, 73km for lon
    :param holder_gdf: geodataframe containing holders with their location (GeoDataFrame) (pos as Point in 'geometry')
    :return: closest_holder : (GeoDataFrame with only 1 line),
             holder_near : (GeoDataFrame),
             distance from the source point to the nearest holder : (degrees)
    """

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
    closest_holder = closest_holder.to_crs(crs)

    holder_near = all_holder.loc[all_holder.intersects(src_point.buffer(distance+0.003))]
    holder_near = holder_near.to_crs(crs)

    return closest_holder, holder_near, distance


def get_holder_square(carre, search_dist, holder_gdf, crs='epsg:4326', ax=None):
    """
    Take 4 points in "carre" (square) based on his diagonals and call get_holder_point() for each of them
    Stock the ids of nearest holders in a list of 4 and all ids of holders considered as near ('distance to nearest' + ~300meters)
    :param carre: square as reference to find near holders : (POLYGON, simple shape and not DataFrame or Series)
    :param search_dist: maximum radius for search in degrees: (float) | 1 degree ~= 111km for lat, 73km for lon
    :param holder_gdf: geodataframe containing holders with their location (GeoDataFrame) (pos as Point in 'geometry')
    :param ax: (optional) reference to the first plot for visualisation, None = no visualisation
    :return: holder_closest : (list) of the 4 nearest holder to the square, can be the same but always with a length of 4
             holder_next_to : (set) of all different id of holders considered as near of the square, only unique id
    """

    corner_list = carre.exterior.coords[0:4]
    holder_next_to = set()
    holder_closest = []

    diag1 = LineString([corner_list[0], corner_list[2]])
    diag2 = LineString([corner_list[1], corner_list[3]])

    x = diag1.intersection(diag2)

    for i in range(4):

        line = LineString([corner_list[i], (x.x, x.y)])
        src_pt = line.interpolate(0.5, normalized=True)

        # for i in range(1, 4, 2):
        #     for j in range(1, 4, 2):
        #         x = perimeter.interpolate(i/16, normalized=True).x
        #         y = perimeter.interpolate(-j/16, normalized=True).y
        #         src_pt = Point(x, y)

        r = get_holder_point(src_pt, search_dist, holder_gdf, crs)
        holder_closest.append(r[0]['ID_SUP'].iloc[0])

        for h in r[1]['ID_SUP']:
            holder_next_to.add(h)

        # ==================|| Visual ||======================================================== #
        if ax is not None:
            r[0].plot(ax=ax, color='red', zorder=5)
            r[1].plot(ax=ax, color="orange", zorder=4)
            # interior = src_pt.buffer(r[2]).exterior.coords[::-1]
            ring_sup = Polygon(src_pt.buffer(r[2] + 0.003).exterior)  # , [interior]
            perimeter_max = src_pt.buffer(search_dist)
            fg = GeoSeries([src_pt, ring_sup, perimeter_max], crs='epsg:4326')
            figure = gpd.GeoDataFrame(geometry=gpd.GeoSeries(fg, crs='epsg:4326'))
            figure = figure.to_crs(crs)
            figure.loc[[0], 'geometry'].plot(ax=ax, color='green', zorder=3)
            figure.loc[[1], 'geometry'].plot(ax=ax, color='none', edgecolor='red', zorder=2)
            figure.loc[[2], 'geometry'].plot(ax=ax, color='none', edgecolor='green', linewidth=1, zorder=2)
        # ======================================================================================= #

    return holder_closest, holder_next_to


def show_holder_around(file_path, pos_in_file=0, lon=None, lat=None, search_dist=0.15, crs='epsg:4326'):  # Paris: 2.207737, 48.921505 180000.csv, # paumé: 15790 140000.csv
    """
    Display a map of French department with all file's squares and informations about the specific square selected.
    Legend: White square = square present in the file
            Blue square = square selected
            Green point = 4 source points of the square from which are find near holder
            Red point = nearest holder of source points (so [1, 4] red point displayed)
            Red circle = field in which are the other near holder (radius = distance to the nearset + ~300meters)
            Orange point = other holder in the red circles
            Green circle = maximum distance from which are selected the holder to the distance comparison
    :param file_path: path of the square file : (String)
    :param pos_in_file: line position of the selected square : (int)
    :param lon: longitude of a point within the square in degrees: (float)
    :param lat: latitude of a point within the square in degrees: (float)
    :param search_dist: maximum radius for search in degrees: (float) | 1 degree ~= 111km for lat, 73km for lon
    """

    gdf_carre = carresfile_to_dataframe(file_path, crs=crs)

    if lon is not None and lat is not None:
        p = Point(lon, lat)

        carre_to_show = gdf_carre.loc[gdf_carre.geometry.contains(Point(lon, lat).buffer(0.00000005)), 'geometry']  # Paris: 2.207737, 48.921505 180000.csv | paumé: 15790 140000.csv

    else:
        carre_to_show = gdf_carre.loc[[pos_in_file], 'geometry']

    holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
    geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
    holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

    dept = gpd.read_file('departements-contour/departements-20180101.shp')
    dept.crs = 'epsg:4326'
    selected_col = ['code_insee', 'geometry']
    dept = dept[selected_col]
    dept = dept.loc[dept["code_insee"].isin(list(filter(lambda x: "97" not in x, dept['code_insee'])))]

    dept = dept.to_crs(crs)
    ax = dept.plot(color='White', edgecolor='k', linewidth=0.5, zorder=0)

    r = get_holder_square(carre_to_show.iloc[0], search_dist, holder_gdf, crs, ax)

    gdf_carre = gdf_carre.to_crs(crs)
    gdf_carre.plot(ax=ax, color='none', edgecolor='k', linewidth=0.25, zorder=1)
    carre_to_show = carre_to_show.to_crs(crs)
    carre_to_show.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25, zorder=2)


    print('Nearest holder:', r[0])
    print("All near holders: ", r[1])

    plt.show()


def add_holder_to_square(file_path, search_dist=0.15):

    holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
    geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
    holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

    gdf_carre = carresfile_to_dataframe(file_path)
    gdf_carre['SupPlusProche'] = None
    gdf_carre['ToutSupProche'] = None

    i = 0
    bar = Bar('Adding holder', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=gdf_carre['num'].size)
    for idx, geom in gdf_carre.iterrows():
        carre = geom[gdf_carre.geometry.name]
        r = get_holder_square(carre, search_dist, holder_gdf)

        gdf_carre.at[idx, 'SupPlusProche'] = "-".join(str(e) for e in r[0])
        gdf_carre.at[idx, 'ToutSupProche'] = "-".join(str(e) for e in r[1])
        bar.next()
    bar.finish()

    print("Writing file...")
    gdf_carre.to_csv('tables/carresSup/carres1800000.csv', sep=';', columns=['num', 'IDsurface', 'IDcrs', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'SupPlusProche', 'ToutSupProche'])


# Start time exec
start_time = time.time()
show_holder_around('tables/carres/carres1800000.csv', lon=2.207737, lat=48.921505)
# show_holder_around('tables/carres/carres1800000.csv',  lon=2.207737, lat=48.921505, crs='epsg:3395')
# add_holder_to_square('tables/carres/carres1800000.csv')

# Show execution time
print("Temps d execution total: %s secondes ---" % (time.time() - start_time))

plt.show()

# res = init_files()
# print("Nb lignes support: ", len(res[0]))
# print("Nb lignes départements: ", len(res[1]))
# print("Nb lignes carres: ", len(res[2]))