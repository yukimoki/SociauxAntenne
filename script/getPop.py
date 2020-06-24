# importing the requests library 
import requests 
import csv

# api-endpoint 
URL = 'http://geo.api.gouv.fr/communes'#16102
 
r = requests.get(url = URL )

# extracting data in json format 
data = r.json() 
header = ["code_postal","nom","population"]

with open('tables/getPopCodePostal.csv', 'w', encoding='UTF-8', newline='') as file_carre:
	csv_carre_writer = csv.writer(file_carre, delimiter=';')
	csv_carre_writer.writerow(header)
	for item in data:
		if("population" in item):
			row = [str(item["codesPostaux"]).replace("[", "").replace("]", "").replace("'", "").replace(", ", "-"), item["nom"], item["population"]]
			csv_carre_writer.writerow(row)