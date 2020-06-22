import os

if not os.path.exists('../statistiques') :
	os.mkdir('../statistiques')

if not os.path.exists('../statistiques/emetteur_population_support'):
	os.mkdir('../statistiques/emetteur_population_support')

if not os.path.exists('../statistiques/emetteur_population_support/StatToutOperateurConfondu'):
	os.mkdir('../statistiques/emetteur_population_support/StatToutOperateurConfondu')

if not os.path.exists('../statistiques/emetteur_population_support/StatParOperateur'):
	os.mkdir('../statistiques/emetteur_population_support/StatParOperateur')

if not os.path.exists('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne'):
	os.mkdir('../statistiques/emetteur_population_support/StatParOperateurMemeOrdonne')

if not os.path.exists('../statistiques/emetteur_population_support/StatParAnnee'):
	os.mkdir('../statistiques/emetteur_population_support/StatParAnnee')