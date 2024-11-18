#importing necessary packages
import numpy as np
import pandas as pd
import requests
import os

#loading in csv file
Season_All_22_23 = pd.read_csv('E0.csv')
Season_All_22_23.head(10)
print(Season_All_22_23.info())
Season_All_22_23.describe()

#loading in all additional .csv files
additional_files = ['B1.csv', 'D1.csv', 'D2.csv', 'E1.csv', 'E2.csv', 'F1.csv', 'F2.csv', 'G1.csv', 'I1.csv',
                        'I2.csv', 'N1.csv', 'P1.csv', 'SC0.csv', 'SP1.csv', 'SP2.csv', 'T1.csv']
additional_dfs = [pd.read_csv(file) for file in additional_files]

#merging additional dfs into single dataframe
Season_All_22_23 = pd.concat([Season_All_22_23] + additional_dfs, ignore_index = True)
print(Season_All_22_23.info())
Season_All_22_23.head(1)

#defining what columns are needed for simplified model
selected_columns = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
Scores_Results_22_23 = Season_All_22_23[selected_columns]
Scores_Results_22_23.head(5)

#recoding how full-time result is represented
recoding_dict = {'H':1, 'D':0.5, 'A':0}
Scores_Results_22_23['FTR'] = Scores_Results_22_23['FTR'].replace(recoding_dict)
Scores_Results_22_23.head(5)

#creating a list of club names
club_names = set(Scores_Results_22_23['HomeTeam'])
for club in club_names:
    print(club)

#populating ELO table with all clubs
club_names_list = list(club_names)
ClubELO = pd.DataFrame({
    'Club': club_names_list,
    'ELO': 1000
})

print(ClubELO)

# Defining ELO constants
k = 40         # ELO factor, can be adjusted
home_adv = 30  # Additional ELO points for the home team
home_elo = 1000
away_elo = 1000

# Defining function to calculate ELO score
def calculate_elo_update(home_elo, away_elo, actual_home_score, k, home_adv):
    # Adjusting home ELO for home advantage
    home_elo_adjusted = home_elo + home_adv

    # Calculating expected scores
    expected_home_score = 1 / (1 + 10 ** ((away_elo - home_elo_adjusted) / 400))

# Sort the DataFrame by date in ascending order
Scores_Results_22_23 = Scores_Results_22_23.sort_values(by='Date').reset_index(drop=True)

# Iterate over each match in the sorted Scores_Results_22_23 DataFrame
for _, match in Scores_Results_22_23.iterrows():
    home_team = match['HomeTeam']
    away_team = match['AwayTeam']
    outcome = match['FTR']  # 'FTR' gives the actual score for the home team: 1.0 (home win), 0.5 (draw), 0.0 (away win)

    # Retrieve current Elo ratings for both teams
    home_elo = ClubELO.loc[ClubELO['Club'] == home_team, 'ELO'].values[0]
    away_elo = ClubELO.loc[ClubELO['Club'] == away_team, 'ELO'].values[0]
    
    # Calculate new Elo ratings
    new_home_elo, new_away_elo = calculate_elo_update(home_elo, away_elo, outcome, k, home_adv)
    
    # Update the ClubELO DataFrame with the new ratings
    ClubELO.loc[ClubELO['Club'] == home_team, 'ELO'] = new_home_elo
    ClubELO.loc[ClubELO['Club'] == away_team, 'ELO'] = new_away_elo

# Display updated ClubELO DataFrame
print(ClubELO)


with open("ELOcode.py", "r") as file:
    for line in file:
        print(repr(line))