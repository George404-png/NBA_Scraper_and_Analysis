#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 12:18:26 2021

@author: george
"""
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playbyplay
from nba_api.stats.endpoints import BoxScoreSummaryV2
from nba_api.stats.endpoints import BoxScoreTraditionalV2
from nba_api.stats.endpoints import LeagueGameLog
import pandas as pd
from tqdm import tqdm
import datetime


teams = teams.get_teams()
GSW = [x for x in teams if x['full_name'] == 'Golden State Warriors'][0]
GSW_id = GSW['id']

all_teams_id = [x['id'] for x in teams]

all_games = pd.DataFrame()

games = LeagueGameLog(season='2019').get_data_frames()[0]
games_home = games[games['MATCHUP'].str.contains('vs.')]
games_away = games[games['MATCHUP'].str.contains('@')]
game_id = games_home['GAME_ID'].values

Stats = pd.DataFrame(columns = ['Game_ID','Home_ID', 'Away_ID', 'Attendance', 'Points_Home','Points_Away','Fouls_Home','Fouls_Away','Referee_1','Referee_2','Referee_3'])


for game in tqdm(game_id):
    dfs = BoxScoreSummaryV2(game).get_data_frames()
    Attendance = dfs[4]['ATTENDANCE'].values[0]
    Homeid = dfs[7]['HOME_TEAM_ID'].values[0]
    Awayid = dfs[7]['VISITOR_TEAM_ID'].values[0]
    pointsh = games_home[games_home['GAME_ID'] == game]['PTS'].values[0]
    pointsa = games_away[games_away['GAME_ID'] == game]['PTS'].values[0]
    foulsh = games_home[games_home['GAME_ID'] == game]['PF'].values[0]
    foulsa = games_away[games_away['GAME_ID'] == game]['PF'].values[0]
    ref1 = dfs[2]['OFFICIAL_ID'].values[0]
    ref2 = dfs[2]['OFFICIAL_ID'].values[1]
    ref3 = dfs[2]['OFFICIAL_ID'].values[2]
    Stats = Stats.append({'Game_ID':game,'Home_ID':Homeid,'Away_ID':Awayid, 'Attendance':Attendance,'Points_Home':pointsh,'Points_Away':pointsa,'Fouls_Home':foulsh,'Fouls_Away':foulsa,'Referee_1':ref1,'Referee_2':ref2,'Referee_3':ref3}, ignore_index=True)
    
Stats.to_csv('/Users/george/Desktop/NBA_Stats.csv')