from bs4 import BeautifulSoup

import pandas as pd

from io import StringIO

import re
import requests

from datetime import datetime, timedelta

import re 
from random import uniform
from io import StringIO

adv = pd.read_excel(r'files/players/archives.xlsx').set_index('Competition')

def compet_df_adv():
    global adv
    print('Récupération du tableau initial...')
    """Class to retrieve all codes of masculine competition from fbref pandas is needed"""
    empty_list = []
    response = requests.get("https://fbref.com/fr/comps/").text.replace('<!--', '').replace('-->', '')

    soup = BeautifulSoup(response, 'html.parser')
    tbody = soup.find_all('tbody')
    for masc in tbody :
        for link in masc.find_all('tr',{'class':'gender-m'}):
            empty_list.append(re.search('/(?!fr)(?!comps)([\w]+)/',link.find('a')['href']).group(1))

    
    df = pd.concat(pd.read_html(StringIO(response)),axis = 0, ignore_index= True)
    df = df.loc[df['Sexe']=='H']
    df['Codes'] = empty_list
    df.set_index(df.columns[0],inplace=True)
    df.drop(df.iloc[90:112].index,inplace=True)
    df.drop(['FIFA Confederations Cup','International Friendlies (M)','UEFA Super Cup','OFC Nations Cup'],inplace=True)
    test=[]
    for x,y in df.iterrows():
        if len(y['Dernière saison']) == 4:
            test.append(1)
        else:
            test.append(0)
    df['Calendaire']=test
    years_inf = []
    years_sup = []
    print('En attente des index...')
    for a,b in df.iterrows():
        if b['Calendaire'] == 0:
            years_inf.append(re.findall('(\d+)-(\d+)',b['Dernière saison'])[0][0])
            years_sup.append(re.findall('(\d+)-(\d+)',b['Dernière saison'])[0][1])
        else:
            years_inf.append(b['Dernière saison'])
            years_sup.append(b['Dernière saison'])
    years_inf = [int(years) for years in years_inf]
    years_sup = [int(years) for years in years_sup]
    df['year_inf'] = years_inf
    df['year_sup'] = years_sup
    df = df[df['Codes']!='79']
    df = df[df['Codes']!='76']
    df = df[df['Codes']!='68']
    df = df[df['Codes']!='Big5']
    print('Fusion en cours')
    df = pd.merge(df, adv, left_index=True, right_index=True, how='outer').dropna(subset='Ctr')
    df=df.loc[~df.index.duplicated(keep='first')].iloc[:,0:10]
    
    return df




"""def age_to_birthdate_timestamp(df_merged):
    # Obtenir la date actuelle
    annees = df_merged['Âge'].str.extract('(.*)-').astype(float)
    jours= round(df_merged['Âge'].str.extract('-(.*)').astype(float)/365.25,3)
    ages = annees+jours

    df_merged['Âge'] = annees+jours

    # Filtrer les lignes où la colonne 'Âge'
    ages_non_na = df_merged.loc[~df_merged['Âge'].isna(), 'Âge']

    current_date = datetime.today()
    
    # Calculer les dates de naissance approximatives
    birthdates = current_date - ages_non_na.apply(lambda x: timedelta(days=x * 365.25)) - timedelta(days=1)
    
    # Mettre à jour la colonne 'Naissance' du DataFrame
    df_merged.loc[ages_non_na.index, 'Naissance'] = birthdates
    
    return df_merged"""