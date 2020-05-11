import csv

# Initialize the list of mobile telephone emitter type (trie.txt)
with open('../trie.txt', newline='') as trieFile:
    typeMobile = trieFile.read().splitlines()

# list of mobile telephone emitter & station/antenna/holder with > 1 mobile telephone emitter
listMobileEmitter = set()
listMobileStation = set()
listMobileAntenna = set()
listMobileHolder = set()

# create and write new files
for element in ["EMETTEUR", "STATION", "ANTENNE", "SUPPORT"]:
    print(element)
    cpt = 0
    with open('tables/SUP_'+element+'.txt', 'r', encoding='latin-1') as supFile:
        fileReader = csv.reader(supFile, delimiter=';')

        with open('tables/MOBILE_'+element+'.txt', 'w') as newFile:
            newFileWriter = csv.writer(newFile, delimiter=';')
            newFileWriter.writerow(next(fileReader))
            for row in fileReader:

                # EMITTER FILE
                if element == "EMETTEUR":
                    if row[1] in typeMobile:
                        cpt += 1
                        newFileWriter.writerow(row)
                        listMobileEmitter.add(row[0])
                        listMobileStation.add(row[2])
                        listMobileAntenna.add(row[3])

                # STATION FILES
                elif element == "STATION":
                    if row[0] in listMobileStation:
                        cpt += 1
                        newFileWriter.writerow(row)

                # ANTENNA FILES
                elif element == "ANTENNE":
                    if row[1] in listMobileAntenna:
                        cpt += 1
                        newFileWriter.writerow(row)
                        listMobileHolder.add(row[7])

                # HOLDER FILES
                else:
                    if (row[0] in listMobileHolder) and (row[1] in listMobileStation):
                        cpt += 1
                        newFileWriter.writerow(row)

    print(cpt, ' lines written\n----------------------')
