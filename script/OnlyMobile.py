# -*-coding:UTF-8 -*
import csv
import time


def sort_by_type():
    """
    Sort the 'tables/SUP_***.txt' files by emitter type include in the 'typeEMRfilter' file
    Sorted tables are create in tables/ dir as MOBILE_***.txt
    :return:
    """
    print("||----SORT FUNCTION----||")

    # Initialize the list of mobile telephone emitter type (typeEMRfilter.txt)
    with open('typeEMRfilter.txt', newline='') as trieFile:
        type_mobile = trieFile.read().splitlines()

    # list of mobile telephone emitter & station/antenna/holder with > 1 mobile telephone emitter
    list_mobile_emitter = set()
    list_mobile_station = set()
    list_mobile_antenna = set()
    list_mobile_holder = set()

    # create and write new files
    for element in ["EMETTEUR", "STATION", "ANTENNE", "SUPPORT"]:
        print(element)
        cpt = 0
        with open('tables/SUP_' + element + '.txt', 'r', encoding='latin-1') as supFile:
            file_reader = csv.reader(supFile, delimiter=';')

            with open('tables/MOBILE_' + element + '.txt', 'w') as newFile:
                new_file_writer = csv.writer(newFile, delimiter=';')

                # Rewrite the header to the new file
                new_file_writer.writerow(next(file_reader))

                for row in file_reader:

                    # EMITTER FILE
                    if element == "EMETTEUR":
                        if row[1] in type_mobile:
                            cpt += 1
                            new_file_writer.writerow(row)
                            list_mobile_emitter.add(row[0])
                            list_mobile_station.add(row[2])
                            list_mobile_antenna.add(row[3])

                    # STATION FILES
                    elif element == "STATION":
                        if row[0] in list_mobile_station:
                            cpt += 1
                            new_file_writer.writerow(row)

                    # ANTENNA FILES
                    elif element == "ANTENNE":
                        if row[1] in list_mobile_antenna:
                            cpt += 1
                            new_file_writer.writerow(row)
                            list_mobile_holder.add(row[7])

                    # HOLDER FILES
                    else:
                        if (row[0] in list_mobile_holder) and (row[1] in list_mobile_station):
                            cpt += 1
                            new_file_writer.writerow(row)

        print(cpt, ' lines written\n----------------------')

    print("||----SORT FINISHED----||")


def create_tables():
    """
    Generate the new database from MOBILE_***.txt file to /finalDB dir location
    """

    # Open all files needed and create the reader/writer
    holder_file = open('tables/finalDB/SUPPORT.csv', 'w')
    csv_holder_writer = csv.writer(holder_file, delimiter=';')
    holder_import = open('tables/MOBILE_SUPPORT.txt', 'r')
    csv_holder_import = csv.reader(holder_import, delimiter=';')

    antenna_file = open('tables/finalDB/ANTENNE.csv', 'w')
    csv_antenna_writer = csv.writer(antenna_file, delimiter=';')
    antenna_import = open('tables/MOBILE_ANTENNE.txt', 'r')
    csv_antenna_import = csv.reader(antenna_import, delimiter=';')

    emitter_file = open('tables/finalDB/EMETTEUR.csv', 'w')
    csv_emitter_writer = csv.writer(emitter_file, delimiter=';')
    emitter_import = open('tables/MOBILE_EMETTEUR.txt', 'r')
    csv_emitter_import = csv.reader(emitter_import, delimiter=';')

    # Write new file header
    header = ["ID_SUP", "NM_LONGITUDE", "NM_LATITUDE", "NM_NB_ANT_D", "NM_NB_ANT_N", "NM_CD_POSTAL"]
    csv_holder_writer.writerow(header)

    header = ["ID_ANT", "ID_SUP", "FG_RAYONEMANT", "NM_DIMENSION", "NM_AZIMUT"]
    csv_antenna_writer.writerow(header)

    header = ["ID_EMR", "ID_SUP", "ID_ANT", "LB_TYPE_EMR", "DATE_EN_SERVICE", "LB_EXPLOITANT"]
    csv_emitter_writer.writerow(header)

    # Skip file header
    next(csv_holder_import)
    next(csv_antenna_import)
    next(csv_emitter_import)

    # Get link between station and operator (for emitter "LB_EXPLOITANT" field)
    station_operator = link_sta_op()

    # Init the dictionary with number of antenna for each holder id :
    # { "ID Holder" : (nbAntenna Directional(D), nbAntenna Omnidirectional(N)) }
    holder_nb_antenna = {}

    # Init the dictionary of correspondence between id antenna and id holder (for emitter table):
    # { "ID Antenna" : "ID Holder" }
    antenna2id_sup = {}

    # Fill 'ANTENNE.csv' table (antenna)
    for ant_row in csv_antenna_import:
        # Create and write the new line
        new_antenna = [ant_row[1], ant_row[7], ant_row[4], ant_row[3], ant_row[5]]
        csv_antenna_writer.writerow(new_antenna)

        # Update antenna / holder correspondence
        antenna2id_sup[ant_row[1]] = ant_row[7]

        # Update antenna numbers (D/N) for each holder
        if not ant_row[7] in holder_nb_antenna:
            if ant_row[4] == 'D':
                holder_nb_antenna[ant_row[7]] = [1, 0]
            else:
                holder_nb_antenna[ant_row[7]] = [0, 1]
        else:
            if ant_row[4] == 'D':
                holder_nb_antenna[ant_row[7]][0] += 1
            else:
                holder_nb_antenna[ant_row[7]][1] += 1

    # Fill 'SUPPORT.csv' table (holder)
    for hdr_row in csv_holder_import:
        if hdr_row[0] in holder_nb_antenna.keys():
            new_holder = [hdr_row[0]]

            # Convert coordinates to longitude and latitude on only 2 fields
            lon = " ".join(hdr_row[7:11]).split(' ')
            lon = dms_to_degrees(lon[0], lon[1], lon[2], lon[3])
            new_holder.append(lon)

            lat = " ".join(hdr_row[3:7]).split(' ')
            lat = dms_to_degrees(lat[0], lat[1], lat[2], lat[3])
            new_holder.append(lat)

            new_holder.append(holder_nb_antenna[hdr_row[0]][0])
            new_holder.append(holder_nb_antenna[hdr_row[0]][1])

            # Delete this key in dict to avoid double holder
            del holder_nb_antenna[hdr_row[0]]

            # Append the final field (postal code) and write the new line
            new_holder.append(hdr_row[17])
            csv_holder_writer.writerow(new_holder)

    # Fill 'EMETTEUR.csv' table (emitter)
    for emr_row in csv_emitter_import:
        # Ignore emitter which refereed to antenna's id or station's id which doesn't exist
        if emr_row[3] in antenna2id_sup.keys() and emr_row[2] in station_operator.keys():
            # Create and write the new line
            new_emitter = [emr_row[0], antenna2id_sup[emr_row[3]], emr_row[3], emr_row[1], emr_row[4], station_operator[emr_row[2]]]
            csv_emitter_writer.writerow(new_emitter)

    # Close all files
    antenna_file.close()
    antenna_import.close()
    emitter_file.close()
    emitter_import.close()


def dms_to_degrees(degrees, minutes, seconds, direction):
    """
    Convert coordinates in (degrees° minutes' seconds" Direction) to degrees only (latitude or longitude)
    :param degrees:
    :param minutes:
    :param seconds:
    :param direction:
    :return: degrees only conversion
    """
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd


def link_sta_op():
    """
    Make the link between station id and operator name
    :return: dictionary {"ID Station" : "Operator Name"}
    """
    with open('tables/SUP_EXPLOITANT.txt') as op_file:
        op_reader = csv.reader(op_file, delimiter=';')
        op_dict = {}
        next(op_reader)
        for op_row in op_reader:
            op_dict[op_row[0]] = op_row[1]

    with open('tables/MOBILE_STATION.txt', 'r') as station_file:
        station_reader = csv.reader(station_file, delimiter=';')
        sta_op_dict = {}
        next(station_reader)
        for sta_row in station_reader:
            sta_op_dict[sta_row[0]] = op_dict[sta_row[1]]

    return sta_op_dict


# Start time exec
start_time = time.time()

sort_by_type()
create_tables()

# Show execution time
print("Temps d execution : %s secondes ---" % (time.time() - start_time))
