print('Importation des modèles')

import pandas as pd
from random import uniform
import os
from selenium.common.exceptions import TimeoutException
from functools import reduce
import time
print('La moitié des modèles sont importés\nImportation des scripts')
from scripts.tools import compet_df_adv
print('Scripts importés\nScrapers en import')
from scripts.scrapers import basics, scrape_shooting_data, scrape_stats_data, scrape_possession_data, scrape_defense_data, scrape_keepers_data, scrape_misc_data, scrape_passing_data, scrape_playingtime_data
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
retries = 0
lap = len(df)
for index,id in df.iterrows():
    print(f'Il reste encore {lap} tours... va faire autre chose de ta vie!')
    lap -= 1
    while retries < max_retries:
        try:
            if id.iloc[7] == 1:
                print('Saison sur l\'année')
                if id.iloc[-1] == 'shooting':
                    print(f'Récupération des frappes en cours dans {index}...')
                    basic = basics(id)
                    list_shooting.append(scrape_shooting_data(basic[0],basic[1],basic[2],basic[3]))

                elif id.iloc[-1] == 'keepersadv':
                    print(f'Récupération des stats gardien en cours dans {index}...')
                    basic = basics(id)
                    list_keepers.append(scrape_keepers_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'playingtime':
                    print(f'Récupération des stats du temps de jeu en cours dans {index}...')
                    basic = basics(id)
                    list_playingtime.append(scrape_playingtime_data(basic[0],basic[1],basic[2],basic[3]))

                elif id.iloc[-1] == 'passing':
                    basic = basics(id)
                    list_passing.append(scrape_passing_data(basic[0],basic[1],basic[2],basic[3]))
                
                elif id.iloc[-1] == 'possession':
                    print(f'Récupération des stats de possession en cours dans {index}...')
                    basic = basics(id)
                    list_possession.append(scrape_possession_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'defense':
                    print(f'Récupération des stats def en cours dans {index}...')
                    basic = basics(id)
                    list_defense.append(scrape_defense_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'misc':
                    print(f'Récupération des stats aléatoires en cours dans {index}...')
                    basic = basics(id)
                    list_misc.append(scrape_misc_data(basic[0],basic[1],basic[2],basic[3]))
                else:
                    print(f'Récupération des stats basiques en cours dans {index}...')
                    basic = basics(id)
                    list_stats.append(scrape_stats_data(basic[0],basic[1],basic[2],basic[3],basic[4]))

                
            else:
                print('Saison en décalé')
                if id.iloc[-1] == 'shooting':
                    print(f'Récupération des frappes en cours dans {index}...')
                    basic = basics(id)
                    list_shooting.append(scrape_shooting_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'keepersadv':
                    print(f'Récupération des stats gardien en cours dans {index}...')
                    basic = basics(id)
                    list_keepers.append(scrape_keepers_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'playingtime':
                    print(f'Récupération des stats du temps de jeu en cours dans {index}...')
                    basic = basics(id)
                    list_playingtime.append(scrape_playingtime_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'passing':
                    basic = basics(id)
                    list_passing.append(scrape_passing_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'possession':
                    print(f'Récupération des stats de possession en cours dans {index}...')
                    basic = basics(id)
                    list_possession.append(scrape_possession_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'defense':
                    print(f'Récupération des stats def en cours dans {index}...')
                    basic = basics(id)
                    list_defense.append(scrape_defense_data(basic[0],basic[1],basic[2],basic[3]))
                elif id.iloc[-1] == 'misc':
                    print(f'Récupération des stats aléatoires en cours dans {index}...')
                    basic = basics(id)
                    list_misc.append(scrape_misc_data(basic[0],basic[1],basic[2],basic[3]))
                else:
                    print(f'Récupération des stats basiques en cours dans {index}...')
                    basic = basics(id)
                    list_stats.append(scrape_stats_data(basic[0],basic[1],basic[2],basic[3],basic[4]))
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
print('Stats des gardien merged')





print('Archivage des dataframes\nArchivafge des joueurs en cours')

directory = 'files/players'
filename = 'FBREF_joueurs_saison_24_25.xlsx'
filepath = os.path.join(directory, filename)

# Créer le dossier s'il n'existe pas
os.makedirs(directory, exist_ok=True)

# Enregistrer le DataFrame dans un fichier Excel
df_merged.to_excel(filepath,ignore_index=True)

print('Joueurs Archivés\nArchivage des gardiens en cours')
directory = 'files/players'
filename = 'gardien_adv_saison_24_25.xlsx'
filepath = os.path.join(directory, filename)
# Créer le dossier s'il n'existe pas
os.makedirs(directory, exist_ok=True)
# Enregistrer le DataFrame dans un fichier Excel
df_full_keeper.to_excel(filepath,ignore_index=True)
directory = 'files/players'
filename = 'gardien_saison_24_25.xlsx'
filepath = os.path.join(directory, filename)
# Créer le dossier s'il n'existe pas
os.makedirs(directory, exist_ok=True)
# Enregistrer le DataFrame dans un fichier Excel
df_full_keeper.to_excel(filepath,ignore_index=True)
print('Gardien Archivés\nScript terminé!')
time.sleep(1)
print('Travail d\'IzmoScouting\nCompte Twitter: @IzmoScouting\nhttps://x.com/IzmoScouting')