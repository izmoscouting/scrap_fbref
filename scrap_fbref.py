from datetime import datetime
print('Début du script à',datetime.now())
print('Importation des modèles')
import pandas as pd
from random import uniform
import os
from selenium.common.exceptions import TimeoutException
from functools import reduce
import time
print('Travail d\'IzmoScouting\nCompte Twitter: @IzmoScouting\nhttps://x.com/IzmoScouting')
time.sleep(1.5)
print('La moitié des modèles sont importés\nImportation des scripts')
from scripts.tools import compet_df_adv
print('Scripts importés\nScrapers en import')
from scripts.scrapers import process_data 
print('Scrapers importés\nRécupération du tableau des compétitions...')

df = compet_df_adv()
df = df.dropna(subset='Sexe')
routes = [['stats','shooting','passing','possession','keepersadv','defense','playingtime','misc']]*len(df.index)
df['routes'] = routes
df = df.explode('routes')
print('Tableau des compétitions récupéré')
print('Récupération des données')

list_misc = []
list_shooting = []
list_keepers = []
list_playingtime = []
list_possession = []
list_stats = []
list_defense = []
list_passing = []
max_retries = 3
lap = len(df)
for index,id in df.iterrows():
    retries = 0
    start_time = time.time()
    print(f'Il reste encore {lap} tours... va faire autre chose de ta vie!')
    lap -= 1
    while retries < max_retries:
        try:    
            process_data(id, index, list_shooting, list_keepers, list_playingtime, list_passing, list_possession, list_defense, list_misc, list_stats)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Cette boucle a pris {elapsed_time}minutes')
            time.sleep(uniform(7,10))
            break
        except TimeoutException:
            print(f"Timeout atteint pour {id.iloc[-1]} de {index}. Tentative {retries + 1} sur {max_retries}.")
            retries += 1
            time.sleep(2 ** retries)

print('Concaténation des dataframes')
df_stat = pd.concat(list_stats,ignore_index=True)
df_pass = pd.concat(list_passing,ignore_index=True)
df_shoot = pd.concat(list_shooting,ignore_index=True)
df_def = pd.concat(list_defense,ignore_index=True)
print('Moitié des Concaténations')
df_keepers = pd.concat(list_keepers,ignore_index=True)
df_misc = pd.concat(list_misc,ignore_index=True)
df_time = pd.concat(list_playingtime,ignore_index=True)
df_poss = pd.concat(list_possession,ignore_index=True)
print('Concaténation finie')


print('Merging des DF')
list_df = [df_stat,df_pass,df_shoot,df_def,df_misc,df_time,df_poss]
list_df_keepers_full = [df_stat,df_keepers.drop(columns=['Naissance','Joueur','Nation','Pos','Équipe','Clt','Âge','90'])]
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Primary_key','Saison'],
                                            how='inner'), list_df)
print('Merged des joueurs de champ',df_merged)
df_full_keeper = reduce(lambda  left,right: pd.merge(left,right,on=['Primary_key','Saison'],
                                            how='inner'), list_df_keepers_full)
print('Gardien merged')





print('Archivage des dataframes\nArchivafge des joueurs en cours')

directory = 'files/players'
filename = 'FBREF_joueurs_saison_24_25.xlsx'
filepath = os.path.join(directory, filename)

# Créer le dossier s'il n'existe pas
os.makedirs(directory, exist_ok=True)

# Enregistrer le DataFrame dans un fichier Excel
df_merged.to_excel(filepath,index=False)

print('Joueurs Archivés\nArchivage des gardiens en cours')
directory = 'files/players'
filename = 'FBREF_gardien_adv_saison_24_25.xlsx'
filepath = os.path.join(directory, filename)
# Créer le dossier s'il n'existe pas
os.makedirs(directory, exist_ok=True)
# Enregistrer le DataFrame dans un fichier Excel
df_full_keeper.to_excel(filepath,index=False)
directory = 'files/players'
filename = 'FBREF_gardien_saison_24_25.xlsx'
filepath = os.path.join(directory, filename)
# Créer le dossier s'il n'existe pas
os.makedirs(directory, exist_ok=True)
# Enregistrer le DataFrame dans un fichier Excel
df_full_keeper.to_excel(filepath,index=False)
print(f'Gardien Archivés\nScript terminé à {datetime.now()}')
time.sleep(1)
print('Travail d\'IzmoScouting\nCompte Twitter: @IzmoScouting\nhttps://x.com/IzmoScouting')