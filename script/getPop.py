# importing the requests library 
import requests 
import csv

# api-endpoint 
URL = 'http://geo.api.gouv.fr/communes'#16102
 
r = requests.get(url = URL )

# extracting data in json format 
data = r.json() 
header = ["code_insee","nom","population"]
file_carre = open('tables/getPopCodePostal.csv', 'w')
csv_carre_writer = csv.writer(file_carre, delimiter=';')
csv_carre_writer.writerow(header)
for item in data:
    if("population" in item):
        csv_carre_writer.writerow([str(item["codesPostaux"]).replace("['","").replace("']",""), item["nom"], item["population"]])


