# -*-coding: UTF-8 -*
import csv
import math
import os
import sys
import time

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geopandas import GeoSeries, GeoDataFrame
from progress.bar import Bar
from shapely.geometry import Polygon, Point, LineString


def departs_shape():
    """
    Link items of carresXXXX.csv with their postal code
    (only global square visualisation)
    """
    dept = gpd.read_file('departements-contour/departements-20180101.shp')
    dept.crs = 'epsg:4326'

    polys = []
    print("Extract square form carresALL.csv")
    with open('tables/carrePlusDe10/carresALL.csv') as carre_file:
        csv_reader = csv.reader(carre_file, delimiter=';')
        next(csv_reader)
        i = 0
        for row in csv_reader:
            if i < 100000:
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


def get_holder_point(src_point, search_dist, holder_gdf, crs='epsg:4326', ax=None):
    """
    Find the nearest holder from a specific point,
    then find all the holder present in a field nearly 300 meters further than the nearest support
    :param crs: chose a specific crs (not recommended)
    :param src_point: point of reference to find near holders : (Point(lat,lon))
    :param search_dist: maximum radius for search in degrees : (float) | 1 degree ~= 111km for lat, 73km for lon
    :param holder_gdf: geodataframe containing holders with their location (GeoDataFrame) (pos as Point in 'geometry')
    :param ax: (optional) reference to the first plot for visualisation, None = no visualisation
    :return: closest_holder : (GeoDataFrame with only 1 line),
             holder_near : (GeoDataFrame),
             distance from the source point to the nearest holder : (degrees)
    """

    all_holder = holder_gdf.loc[holder_gdf.intersects(src_point.buffer(search_dist))]
    unary = all_holder.unary_union
    closest_holder_point = None
    distance = 9999999
    dist_rad = search_dist + 99999

    earth_rad = 6372800  # Earth radius in meters
    for holder_point in enumerate(unary):
        # d = holder_point[1].distance(src_point)
        phi1, phi2 = math.radians(holder_point[1].y), math.radians(src_point.y)
        dphi = math.radians(src_point.y - holder_point[1].y)
        dlambda = math.radians(src_point.x - holder_point[1].x)

        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

        d = 2 * earth_rad * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        if d < distance:
            distance = d
            dist_rad = holder_point[1].distance(src_point)
            closest_holder_point = holder_point

    closest_holder = holder_gdf.loc[holder_gdf.intersects(closest_holder_point[1].buffer(0.00000005))]
    closest_holder = closest_holder.to_crs(crs)

    holder_near = all_holder.loc[all_holder.intersects(src_point.buffer(dist_rad+0.003))]
    holder_near = holder_near.to_crs(crs)

    # ==================|| Visual ||======================================================== #
    if ax is not None:
        closest_holder.plot(ax=ax, color='red', zorder=5)
        holder_near.plot(ax=ax, color="orange", zorder=4)
        # interior = src_pt.buffer(r[2]).exterior.coords[::-1]
        ring_sup = Polygon(src_point.buffer(dist_rad + 0.003).exterior)  # , [interior]
        perimeter_max = src_point.buffer(search_dist)
        fg = GeoSeries([src_point, ring_sup, perimeter_max], crs='epsg:4326')
        figure = gpd.GeoDataFrame(geometry=gpd.GeoSeries(fg, crs='epsg:4326'))
        figure = figure.to_crs(crs)
        figure.loc[[0], 'geometry'].plot(ax=ax, color='green', zorder=3)
        figure.loc[[1], 'geometry'].plot(ax=ax, color='none', edgecolor='red', zorder=2)
        figure.loc[[2], 'geometry'].plot(ax=ax, color='none', edgecolor='green', linewidth=1, zorder=2)
    # ======================================================================================= #

    return closest_holder, holder_near, distance


def get_holder_square(carre, search_dist, holder_gdf, crs='epsg:4326', ax=None):
    """
    Take 4 points in "carre" (square) based on his diagonals and call get_holder_point() for each of them
    Stock the ids of nearest holders in a list of 4 and all ids of holders considered as near ('distance to nearest' + ~300meters)
    :param crs: chose a specific crs (not recommended) : (str)
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

        r = get_holder_point(src_pt, search_dist, holder_gdf, crs, ax)

        holder_closest.append((r[0]['ID_SUP'].iloc[0], r[2]))

        for h in r[1]['ID_SUP']:
            holder_next_to.add(h)

    return holder_closest, holder_next_to


def show_holder_around(file_path, ax, pos_in_file=0, lon=None, lat=None, search_dist=0.15, crs='epsg:4326'):  # Paris: 2.207737, 48.921505 180000.csv, # paumé: 15790 140000.csv
    """
    Display a map of French department with all file's squares and informations about the specific square selected.
    Legend: White square = square present in the file
            Blue square = square selected
            Green point = 4 source points of the square from which are find near holder
            Red point = nearest holder of source points (so [1, 4] red point displayed)
            Red circle = field in which are the other near holder (radius = distance to the nearest + ~300meters)
            Orange point = other holder in the red circles
            Green circle = maximum distance from which are selected the holder to the distance comparison
    :param crs: chose a specific crs (not recommended) : (string)
    :param file_path: path of the square file : (string)
    :param pos_in_file: line position of the selected square : (int)
    :param lon: longitude of a point within the square in degrees: (float)
    :param lat: latitude of a point within the square in degrees: (float)
    :param search_dist: maximum radius for search in degrees: (float) | 1 degree ~= 111km for lat, 73km for lon
    """

    gdf_carre = carresfile_to_dataframe(file_path, crs=crs)

    if lon is not None and lat is not None:
        p = Point(lon, lat)
        carre_to_show = gdf_carre.loc[gdf_carre.geometry.contains(p.buffer(0.00000005)), 'geometry']  # Paris: 2.207737, 48.921505 180000.csv | paumé: 15790 140000.csv

    else:
        carre_to_show = gdf_carre.loc[[pos_in_file], 'geometry']

    holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
    geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
    holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

    r = get_holder_square(carre_to_show.iloc[0], search_dist, holder_gdf, crs, ax)

    gdf_carre = gdf_carre.to_crs(crs)
    gdf_carre.plot(ax=ax, color='none', edgecolor='k', linewidth=0.25, zorder=1)
    carre_to_show = carre_to_show.to_crs(crs)
    carre_to_show.plot(ax=ax, color='blue', edgecolor='k', linewidth=0.25, zorder=2)

    print('Nearest holder:', r[0])
    print("All near holders: ", r[1])

    return ax


def add_holder_to_square(file_path, holder_gdf, gdf_carre, start=1, end=None, search_dist=0.15):
    """
    Create a file based on square file and append 3 columns with:
        - SupPlusProche: id of the nearest holder (int)
        - DistPlusProche: distance to the nearest holder (float, 2 decimals)
        - ToutSupProche: all holder within a radius of nearest dist + ~300 meters (for 4 point of square subdivision)
    :param file_path: path of the square's file: (string)
    :param start: first line number to treat: (int) >= 1
    :param end: last line number to treat: (int) <= total of line
    :param search_dist: maximum radius for search in degrees: (float) | 1 degree ~= 111km for lat, 73km for lon
    """
    # Line number to index
    start -= 1
    if end is None:
        end = gdf_carre["'num'"].size

    gdf_carre["'SupProchePt1'"] = None
    gdf_carre["'SupProchePt2'"] = None
    gdf_carre["'SupProchePt3'"] = None
    gdf_carre["'SupProchePt4'"] = None
    gdf_carre["'IdAllSupProche'"] = None

    gdf_wanted = gdf_carre.iloc[start: end]

    bar = Bar('Adding holder', suffix='%(index)d/%(max)d : %(percent)d%% [%(elapsed_td)s]', max=end-start)
    for idx, geom in gdf_wanted.iterrows():
        carre = geom[gdf_wanted.geometry.name]
        r = get_holder_square(carre, search_dist, holder_gdf)

        gdf_wanted.at[idx, "'SupProchePt1'"] = "'"+str(r[0][0][0])+"-"+str(round(r[0][0][1]))+"'"
        gdf_wanted.at[idx, "'SupProchePt2'"] = "'"+str(r[0][1][0])+"-"+str(round(r[0][1][1]))+"'"
        gdf_wanted.at[idx, "'SupProchePt3'"] = "'"+str(r[0][2][0])+"-"+str(round(r[0][2][1]))+"'"
        gdf_wanted.at[idx, "'SupProchePt4'"] = "'"+str(r[0][3][0])+"-"+str(round(r[0][3][1]))+"'"

        gdf_wanted.at[idx, "'IdAllSupProche'"] = "'"+"-".join(str(e) for e in r[1])+"'"
        bar.next()
    bar.finish()

    print("Writing file...")
    gdf_wanted.to_csv(file_path[:-4]+"["+str(start+1)+"-"+str(end)+"]"+"avecSup.csv", sep=';', columns=["'num'", "'IDsurface'", "'IDcrs'", "'x1'", "'y1'", "'x2'", "'y2'", "'x3'", "'y3'", "'x4'", "'y4'","'SupProchePt1'", "'SupProchePt2'", "'SupProchePt3'", "'SupProchePt4'", "'IdAllSupProche'"], index=False)


def in_line_launcher():
    print("init")
    holder_df = pd.read_csv('tables/finalDB/SUPPORT.csv', delimiter=';')
    geometry = [Point(xy) for xy in zip(holder_df.NM_LONGITUDE, holder_df.NM_LATITUDE)]
    holder_gdf = GeoDataFrame(holder_df, crs='epsg:4326', geometry=geometry)

    gdf_carre = carresfile_to_dataframe(sys.argv[1])

    print("init done")

    return_fork = -1
    step = round((int(sys.argv[3])-int(sys.argv[2]))/int(sys.argv[4]))
    start = int(sys.argv[2])
    end = start + step - 1
    for i in range(int(sys.argv[4])+1):

        if return_fork == 0:
            print("start add holder")
            print(start, end, step)
            add_holder_to_square(sys.argv[1], holder_gdf, gdf_carre, start, end)
            print("Temps d execution processus fils: %s secondes ---" % (time.time() - start_time))
            exit(0)
        else:
            print("new process", i)
            return_fork = os.fork()
            if i > 0:
                start += step
                end = start + step - 1
                if end > int(sys.argv[3]):
                    end = int(sys.argv[3])

    for i in range(int(sys.argv[4])):
        print(os.wait())


# Start time exec
start_time = time.time()

crs = 'epsg:4326'
dept = gpd.read_file('departements-contour/departements-20180101.shp')
dept.crs = 'epsg:4326'
selected_col = ['code_insee', 'geometry']
dept = dept[selected_col]
dept = dept.loc[dept["code_insee"].isin(list(filter(lambda x: "97" not in x, dept['code_insee'])))]
dept = dept.to_crs(crs)
ax = dept.plot(color='White', edgecolor='k', linewidth=0.5, zorder=0)

for i in range(53231, 53237):
    show_holder_around('tables/carres/carres1100000.csv', pos_in_file=i, ax=ax)
for i in range(53628, 53633):
    show_holder_around('tables/carres/carres1100000.csv', pos_in_file=i, ax=ax)
plt.show()

print("Temps d execution total: %s secondes ---" % (time.time() - start_time))


# show_holder_around('tables/carres/carres1800000.csv',  lon=2.207737, lat=48.921505)

