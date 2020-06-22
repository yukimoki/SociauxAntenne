# Stage SociauxAntenne

##### different-type.txt

Le fichier : different-type.txt contient tout les différents type d'émetteurs présents dans la base de donnée initial.

##### trie et triefinal

Le fichier trie contient tout les type pertinent au projet et le fichier triefinal tous ceux pertinent mais condensé.

##### recupdonnéeSUpport 

Le fichier recupdonnéeSUpport permet avec en entré l' id d 'un support d'avoir les informations utiles pour créer l'échantillon.

##### script 

L dossier script contient la majorité des scripts de création de base de données et de graphiques.

Pour fonctionner  ces script ont besoin d'un dossier tables avec les fichier d'entrée. Ce dossier est intégré dans le git ignore.

##### algo.py

Le script algo.py permet d'associer des support a des carré donné. Il s'utilise de la façon suivate : 

*python3 algo.py     <u>nomdufichiercarré</u>      lignedébut           lignefin          nbrprocessus*

```bash
python3 algo.py carresALL.csv 100 200 4
```

Par exemple cette commande cherche dans carresALL.csv du 100e carré au 200e carré réparti sur 4 processus

##### onlymobile

Le script onlymobile permet de crée la base de donnée à partir des fichier SUP, il est nécessaire d'avoir ces fichier dans le dossier tables. et li est nécessaire d'avoir un dossier finalDB dans le dossier tables.

##### carre.py

Le script carre.py permet de récupéré uniquement les carrées de statistiques avec plus de 10 habitant. Il est nécessaire d'avoir un dossier carrePlusDe10 dans tables et d'avoir le fichier carres-stats-avec-nb-antennes issu du répertoire Dante.

#####  formatcarre.py 

Le script formatcarre.py permet de créer CarresDistSupProche.csv dans le dossier tables/finalDB. Ce script nécéssite finalcarres.csv dans le dossier carrePlusDe10 et généré avec :

 ```bash
mv carresALL\[1-* finalcarres.csv
tail -n +2 -q carresALL\[*  >> finalcarres.csv
 ```

##### getPOp.py

Le script getPOp.py permet de généré, à partir de l'api gouvernementale le fichier tables/getPopCodePostal.csv.



##### newlinearstatpop.py

Permet de générer le nuage de point interactif et de le sauvegarder dans tables.

##### statfromlocation.py

Permet de générer le graphique du nombre de support en fonction du nombre d'habitant dans la commune dans /tables.

# OnlyMobile.py

! the script must be executed with pyton3 in his own dir

The script takes all *SUP_\** tables in tables dir and wrtite new ones *MOBILE_\** in the same dir.
New tables only include emitters with type is in *typeEMRfilter.txt* or other elements holding this type of emitter.

## File needed
| Files              | Description |
|--------------------|-------------|
| ./OnlyMobile.py    | Source code |
| Import (csv, time) | |
| ./tables/SUP_?.txt | Dir with all tables to sort (SUPPORT, ANTENNE, STATION, EMETTEUR) |
| *./tables/SUP_EXPLOITANT.txt* | Link between id and name of operator |
| ./typeEMRfilter    | File with all emitters types to filter (initialy mobile network)|
