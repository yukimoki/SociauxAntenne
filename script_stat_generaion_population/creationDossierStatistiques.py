import os

if not os.path.exists('../statistiques') :
	os.mkdir('../statistiques')

if not os.path.exists('../statistiques/emetteur_population_support'):
	os.mkdir('../statistiques/emetteur_population_support')

if not os.path.exists('../statistiques/emetteur_population_support'):
	os.mkdir('../statistiques/emetteur_population_support/StatToutOperateurConfondu')

if not os.path.exists('../statistiques/emetteur_population_support'):
	os.mkdir('../statistiques/emetteur_population_support/StatParOperateur')

if not os.path.exists('../statistiques/emetteur_population_support'):
	os.mkdir('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne')