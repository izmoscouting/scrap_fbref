from bs4 import BeautifulSoup
import pandas as pd


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import re
from random import uniform
from selenium import webdriver
from io import StringIO
import time

adv = pd.read_excel(r'files/players/archives.xlsx').set_index('Competition')

def basics(id):
    if id.iloc[7] == 1:
        url = f"https://fbref.com/fr/comps/{id.iloc[6]}/{int(id.iloc[9])}/{id.iloc[-1]}/"

        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(15)

        try:
            driver.get(url)
        except:
            driver.refresh()
            driver.get(url)

        # Gérer les pop-ups
        deny = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/button[3]'))
        )
        deny.click()

        # Localiser la table principale
        try:
            table = WebDriverWait(driver, uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[4]'))
            )
        except:
            unwrap_table = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[6]/div[3]/button'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(unwrap_table).perform()
            unwrap_table.click()

            table = WebDriverWait(driver, uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[6]'))
            )

        # Extraire le HTML de la page
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Lire le tableau HTML
        dfs = pd.read_html(StringIO(str(soup.find_all('table'))), header=1)[2]

        # Nettoyer le DataFrame
        dfs.drop_duplicates('Clt', inplace=True)
        dfs.drop(columns='Matchs', inplace=True)
        dfs = dfs[dfs['Joueur'] != 'Joueur']

        # Extraire les clés primaires
        profil = []
        primary_key = []
        try:
            unwrap_table2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[6]/div[3]/button[2]')))

            actions = ActionChains(driver)
            actions.move_to_element(unwrap_table2).perform()
            time.sleep(1)
            unwrap_table2.click()
            time.sleep(0.8)
            primo = table.find_elements(By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[6]/table/tbody/tr/td[1]/a')
            jm_key = len(dfs.columns)
            journaux_match = table.find_elements(By.XPATH, f'/html/body/div[4]/div[6]/div[3]/div[6]/table/tbody/tr/td[{jm_key}]/a')
        except:

            primo = table.find_elements(By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[4]/table/tbody/tr/td[1]/a')
            jm_key = len(dfs.columns)
            journaux_match = table.find_elements(By.XPATH, f'/html/body/div[4]/div[6]/div[3]/div[4]/table/tbody/tr/td[{jm_key}]/a')

        for row in primo:
            href = row.get_attribute('href')
            profil.append(href)
            primary_key.append(re.findall(r'(?<=/joueurs/)(.*?)(?=/)',href)[0])
        
    else:
    
        url = f"https://fbref.com/fr/comps/{id.iloc[6]}/{int(id.iloc[8])}-{int(id.iloc[9])}/{id.iloc[-1]}/"

        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(15)

        try:
            driver.get(url)
        except:
            driver.refresh()
            driver.get(url)

        # Gérer les pop-ups
        deny = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/button[3]'))
        )
        deny.click()

        # Localiser la table principale
        try:
            table = WebDriverWait(driver, uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[4]'))
            )
        except:
            unwrap_table = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[6]/div[3]/button'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(unwrap_table).perform()
            unwrap_table.click()

            table = WebDriverWait(driver, uniform(3, 5)).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[6]'))
            )

        # Extraire le HTML de la page
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Lire le tableau HTML
        dfs = pd.read_html(StringIO(str(soup.find_all('table'))), header=1)[2]

        # Nettoyer le DataFrame
        dfs.drop_duplicates('Clt', inplace=True)
        dfs.drop(columns='Matchs', inplace=True)
        dfs = dfs[dfs['Joueur'] != 'Joueur']

        # Extraire les clés primaires
        profil = []
        primary_key = []
        try:
            unwrap_table2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[6]/div[3]/button[2]')))

            actions = ActionChains(driver)
            actions.move_to_element(unwrap_table2).perform()
            time.sleep(1)
            unwrap_table2.click()
            time.sleep(0.8)
            primo = table.find_elements(By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[6]/table/tbody/tr/td[1]/a')
            jm_key = len(dfs.columns)
            journaux_match = table.find_elements(By.XPATH, f'/html/body/div[4]/div[6]/div[3]/div[6]/table/tbody/tr/td[{jm_key}]/a')
        except:

            primo = table.find_elements(By.XPATH, '/html/body/div[4]/div[6]/div[3]/div[4]/table/tbody/tr/td[1]/a')
            jm_key = len(dfs.columns)
            journaux_match = table.find_elements(By.XPATH, f'/html/body/div[4]/div[6]/div[3]/div[4]/table/tbody/tr/td[{jm_key}]/a')

        for row in primo:
            href = row.get_attribute('href')
            profil.append(href)
            primary_key.append(re.findall(r'(?<=/joueurs/)(.*?)(?=/)',href)[0])
            
    return dfs,driver,primary_key,journaux_match,profil

def scrape_stats_data(dfs,driver,primary_key,journaux_match,profil):
    dfs = dfs.drop(columns=[col for col in dfs.columns if re.search(r'\.1$', col)])
    jm_link = []
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        jm_link.append(href)
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)',href)[0])

    driver.quit()

    dfs['Matchs'] = jm_link
    dfs['Profil'] = profil
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison


    return dfs

def scrape_shooting_data(dfs,driver,primary_key,journaux_match):
    # Nettoyer les colonnes
    dfs.drop(columns=['Naissance', 'Joueur', 'Nation', 'Âge', '90','Pos','Équipe','Clt', 'Buts', 'PénM', 'PénT', 'xG', 'npxG'], inplace=True)
    dfs.rename(columns={'Dist': 'Dist MTir'}, inplace=True)

    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison

    return dfs

def scrape_passing_data(dfs,driver,primary_key,journaux_match):
    dfs.drop(columns=['Naissance','Joueur','Nation','Âge','Pos','Équipe','Clt','90','PD','xAG','PrgP'],inplace=True)
    dfs.rename(columns={'Cmp.1':'Passes TR','Att.1':'Passes TT','Cmp%.1':'%Passes TR','TotDist':'Dist Passes','DistBut':'Dist Passes_v_But',\
                    'Cmp.2':'Passes CR','Att.2':'Passes CT','Cmp%.2':'%Passes CR','Cmp.3':'Passes MR','Att.3':'Passes MT','Cmp%.3':'%Passes MR','Cmp.4':'Passes LR','Att.4':'Passes LT','Cmp%.4':'%Passes LR','PPA':'PsrfRep','1/3':'Passes 1/3'},inplace=True)

    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison


    return dfs

def scrape_possession_data(dfs,driver,primary_key,journaux_match):
    dfs.drop(columns=['Naissance','Joueur','Nation','Pos','Équipe','Clt','Âge','90','PrgC'],inplace=True)
    dfs.rename(columns={'Action de jeu':'B. Touches w/oCPA','Touches':'B. Touches','SurfRépDéf':'BT SurfRepDef','ZDéf':'BT Zdef','MilTer':'BT MilTer',\
                    'ZOff':'BT ZOff','SurfRépOff':'BT SurfRepOff','Att':'Drb Tente','Succ':'Drb Reussi','Succ%':'%Drb R','TKld':'Faute Subie','Tkld%':'%FSubie','Balle au pied':'Controle','TotDist':'TotDist BaP','DistBut':'DistvBut BaP','1/3':'C1/3','Manqué':'C. Manque','Perte':'Depossede','Rec':'P. Recu'},inplace=True)

    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison

    return dfs

def scrape_keepers_data(dfs,driver,primary_key,journaux_match):
    # Nettoyer les colonnes
    dfs.rename(columns={'Pc':'Peno C','CF':'BE CF','Co':'BE Corn.','Cmp.1':'Deg R','Att.1':'Deg T',\
                'Cmp%.1':'%Deg R','Tentatives cadrées (GB)':'Passes T','Lanc':'Passes >35m T','% de lancement.1':'%P>35m','LongMoy':'P LongMoy.1','Att.2':'Deg 6m T.','% de lancement.2':'%Deg >35m T','LongMoy.2':'LongMoy Deg','Adv':'Centres Subis','Stp':'Centres Stp','#ESR':'Def HSR','#ESR/90':'Def HSR/90','DistMoy':'Interv DistMoy'},inplace=True)

    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison
    return dfs

def scrape_defense_data(dfs,driver,primary_key,journaux_match):
    dfs.drop(columns=['Naissance','Joueur','Nation','Âge','Pos','Équipe','Clt','90','Manqués'],inplace=True)
    dfs.rename(columns={'Tcl.1':'Tacles T','ZDéf':'Tcl ZDef','MilTer':'Tcl MilTer','ZOff':'Tcl ZOff','Att':'Tcl o/Drb T',\
                    'Tcl.2':'Tcl o/Drb R','Tcl%':'Tcl o/Drb %R','Tirs':'Tirs Contres','Passe':'Passe Contrees'},inplace=True)
    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison

    return dfs

def scrape_playingtime_data(dfs,driver,primary_key,journaux_match):
    dfs.drop(columns=['Naissance','Joueur','Nation','Âge','90','Pos','Équipe','Clt','MJ','Min','Titulaire','onxG','onxGA','+/-','xG+/-'],inplace=True)
    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison

    return dfs

def scrape_misc_data(dfs,driver,primary_key,journaux_match):
    # Nettoyer les colonnes
    dfs.drop(columns=['Naissance','Joueur','Nation','Âge','Pos','Équipe','Clt','90','CJ','CR','Int','TclR'],inplace=True)
    dfs.rename(columns={'Ftp':'Fte Provoq','Ctr':'CSR T','Gagnés':'DA Gagne','Perdus':'DA Perdu','% gagnés':'%DA Gagne'},inplace=True)

    # Extraire les saisons
    saison = []
    for row in journaux_match:
        href = row.get_attribute('href')
        saison.append(re.findall(r'(?<=/matchs/)(.*?)(?=/)', href)[0])

    driver.quit()

    # Ajouter les données au DataFrame
    dfs['Primary_key'] = primary_key
    dfs['Saison'] = saison

    # Ajouter le DataFrame à la liste
    return dfs