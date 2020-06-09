import csv
import pandas as pd
import numpy as np
import time
from progress.bar import IncrementalBar

# Paths
cStats = 'data/StatsSocioCarres.csv'

# Files

with open(cStats) as carre_file:
    cStats_df = pd.read_csv(carre_file, sep='\s+')
    i = 0
    bar = IncrementalBar('Chargement', max=len(cStats_df))
    for index, row in cStats_df.iterrows():
        bar.next()
        i+= row['poptot']
    bar.finish()
    print(i)