# -*- coding: utf-8 -*-
"""
@author: Rohan
"""

# Imports
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import time

#--------------------------------------------------------------------------------------
# All Players
all_players = players.get_players()
df_players = pd.DataFrame(all_players)

# Keep active players only (recommended)
df_players = df_players[df_players['is_active'] == True].reset_index(drop=True)

# Rename for BI clarity
df_players = df_players.rename(columns={
    'id': 'player_id',
    'full_name': 'player_name'
})

# Select clean columns
df_players = df_players[['player_id', 'player_name', 'first_name', 'last_name', 'is_active']]

print(df_players.head())

#----------------------------------------------------------------------------------------
# All teams
nba_teams = teams.get_teams()
df_teams = pd.DataFrame(nba_teams)

df_teams = df_teams.rename(columns={
    'id': 'team_id',
    'full_name': 'team_name'
})

df_teams = df_teams[['team_id', 'team_name', 'abbreviation', 'city', 'state', 'year_founded']]

print(df_teams.head())

#--------------------------------------------------------------------------------------------
# 2024-2025 Teams Game Log Data
all_team_logs = []

for _, row in df_teams.iterrows():
    team_id = row['team_id']
    team_name = row['team_name']
    
    try:
        print(f"Pulling team logs for {team_name}")
        
        tgl = teamgamelog.TeamGameLog(
            team_id=team_id,
            season='2024-25',
            season_type_all_star='Regular Season'
        )
        
        df_team_log = tgl.get_data_frames()[0]
        df_team_log['TEAM_ID'] = team_id
        
        all_team_logs.append(df_team_log)
        time.sleep(0.6)
        
    except Exception as e:
        print(f"Error with {team_name}: {e}")
        
#-------------------------------------------------------------------------------------------------
# 2024-2025 Player Game Log Data
all_player_logs = []

for _, row in df_players.iterrows():
    player_id = row['player_id']
    player_name = row['player_name']
    
    try:
        print(f"Pulling game log for {player_name}")
        
        pgl = playergamelog.PlayerGameLog(
            player_id=player_id,
            season='2024-25',
            season_type_all_star='Regular Season'
        )
        
        df_player_log = pgl.get_data_frames()[0]
        df_player_log['PLAYER_ID'] = player_id
        
        all_player_logs.append(df_player_log)
        time.sleep(0.6)
        
    except Exception as e:
        print(f"Error with {player_name}: {e}")
        
#---------------------------------------------------------------------------------------
# Cleaning up the data

df_player_gamelogs = pd.concat(all_player_logs, ignore_index=True)

df_player_gamelogs = df_player_gamelogs.rename(columns={
    'PLAYER_ID': 'player_id',
    'Player_ID': 'player_id',
    'Game_ID': 'game_id',
    'GAME_DATE': 'game_date',
    'MATCHUP': 'matchup',
    'WL': 'win_loss',
    'MIN': 'minutes',
    'PTS': 'points',
    'REB': 'rebounds',
    'AST': 'assists',
    'STL': 'steals',
    'BLK': 'blocks',
    'TOV': 'turnovers',
    'FGM': 'fg_made',
    'FGA': 'fg_attempted',
    'FG_PCT': 'fg_pct',
    'FG3M': 'fg3_made',
    'FG3A': 'fg3_attempted',
    'FG3_PCT': 'fg3_pct',
    'FTM': 'ft_made',
    'FTA': 'ft_attempted',
    'FT_PCT': 'ft_pct'
})

fact_player_gamelog = df_player_gamelogs[[
    'player_id',
    'game_id',
    'game_date',
    'matchup',
    'win_loss',
    'minutes',
    'points',
    'rebounds',
    'assists',
    'steals',
    'blocks',
    'turnovers',
    'fg_made',
    'fg_attempted',
    'fg_pct',
    'fg3_made',
    'fg3_attempted',
    'fg3_pct',
    'ft_made',
    'ft_attempted',
    'ft_pct'
]]

print(fact_player_gamelog.head())

df_team_gamelogs = pd.concat(all_team_logs, ignore_index=True)

df_team_gamelogs = df_team_gamelogs.rename(columns={
    'TEAM_ID': 'team_id',
    'Game_ID': 'game_id',
    'GAME_DATE': 'game_date',
    'MATCHUP': 'matchup',
    'WL': 'win_loss',
    'MIN': 'minutes',
    'PTS': 'points',
    'REB': 'rebounds',
    'AST': 'assists',
    'STL': 'steals',
    'BLK': 'blocks',
    'TOV': 'turnovers',
    'FGM': 'fg_made',
    'FGA': 'fg_attempted',
    'FG_PCT': 'fg_pct',
    'FG3M': 'fg3_made',
    'FG3A': 'fg3_attempted',
    'FG3_PCT': 'fg3_pct',
    'FTM': 'ft_made',
    'FTA': 'ft_attempted',
    'FT_PCT': 'ft_pct'
})

fact_team_gamelog = df_team_gamelogs[[
    'team_id',
    'game_id',
    'game_date',
    'matchup',
    'win_loss',
    'minutes',
    'points',
    'rebounds',
    'assists',
    'steals',
    'blocks',
    'turnovers',
    'fg_made',
    'fg_attempted',
    'fg_pct',
    'fg3_made',
    'fg3_attempted',
    'fg3_pct',
    'ft_made',
    'ft_attempted',
    'ft_pct'
]]

print(fact_team_gamelog.head())

#-------------------------------------------------------------------
# Export Data to CSV

desktop_path = r"C:\Users\....\Desktop"

df_players.to_csv(f"{desktop_path}\\DimPlayers.csv", index=False)
df_teams.to_csv(f"{desktop_path}\\DimTeams.csv", index=False)
fact_player_gamelog.to_csv(f"{desktop_path}\\FactPlayerGameLog_2024_25.csv", index=False)
fact_team_gamelog.to_csv(f"{desktop_path}\\FactTeamGameLog_2024_25.csv", index=False)

print("All CSV files saved to Desktop successfully.")
