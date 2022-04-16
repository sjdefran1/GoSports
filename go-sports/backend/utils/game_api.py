# -*- coding: utf-8 -*-
"""
@author: Sam DeFrancisco

 game_api just holds useful functions for gathering game data
 get the last n games of a team
 get all games from this season for a team
 get all games tonight w/ current score and time
 get standings
 
"""
import pandas as pd
import time
import requests

import datetime as dt

from nba_api.stats.endpoints import teamgamelog, teamgamelogs, scoreboardv2
# used for annoying parameters in the api
from nba_api.stats.library.parameters import SeasonType, LeagueID

#from utils.util import get_all_team_nameslist

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}


# returns all games a team has played this year by teamID
def game_logs(teamID):
    gathered = False
    while gathered == False:
        try:
            print(f"\t{teamID} Start...")
            team_log = teamgamelog.TeamGameLog(season='2021', season_type_all_star=SeasonType.regular,\
                                               team_id=teamID, timeout=10)
            gathered = True # nice
            team_log = team_log.get_data_frames()[0]
            print(f"\t{teamID} Finished...")
        except:
            print('Game log retrieval error, sleeping and trying again')
            time.sleep(10)
    return team_log



# returns teams last n games   
def last_n_games(teamID, n):
    team_log = game_logs(teamID)
    try:
        return team_log.iloc[0:n]
    except:
        print("last {n} games unavailable, most likely to many games back")
        return

# returns df w/ each matchup of the day
# df columns ['Home_Team','Away_Team', 'Home_Pts', 'Away_Pts', 'QTR', 'Time']
def games_today():
    score_board_sets = scoreboardv2.ScoreboardV2(day_offset=0, game_date=dt.datetime.now(), league_id='00')
    score_board_sets = score_board_sets.data_sets
    # matchups
    # score_board = score_board[2].get_data_frame()
    # line score [1] live_qtr info [0]
    line_score = score_board_sets[1].get_data_frame()
    live_info = score_board_sets[0].get_data_frame()
    # get rid of pts breakdown, un-needed
    line_score = line_score.drop(columns=['PTS_QTR1','PTS_QTR2','PTS_QTR3','PTS_QTR4','PTS_OT1',\
                                            'PTS_OT2','PTS_OT3', 'PTS_OT4', 'PTS_OT5', 'PTS_OT6', 'PTS_OT7',\
                                            'PTS_OT8','PTS_OT9', 'PTS_OT10'])
    # get rid of useless stuff 
    live_info = live_info.drop(columns=['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'GAME_STATUS_ID',\
                                        'GAMECODE', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID',\
                                        'SEASON','NATL_TV_BROADCASTER_ABBREVIATION', 'HOME_TV_BROADCASTER_ABBREVIATION',\
                                        'AWAY_TV_BROADCASTER_ABBREVIATION', 'WH_STATUS', 'WNBA_COMMISSIONER_FLAG',\
                                        'LIVE_PERIOD_TIME_BCAST'])
   
    # iterate through score_board df
    # every 2 rows is a matchup, but theres no nice way to increment by 2 every iteration
    # so using weird for loop, excepts out of bounds to indicate done
    j=0
    index = 0
    complete = False
    matchups_df = pd.DataFrame(columns=['Home_Team','Away_Team', 'Home_Pts', 'Away_Pts', 'QTR', 'Time', 'Status'])
    while complete == False:
        try:
            j+=2
            # get home & away team pandas.series
            home_team = line_score.iloc[j-1]
            away_team = line_score.iloc[j-2]
            # format to dict for easyily appending to dataframe
            data = {
                'Home_Team': home_team.loc['TEAM_NAME'],
                'Away_Team': away_team.loc['TEAM_NAME'],
                'Home_Pts': home_team.loc['PTS'], 
                'Away_Pts': away_team.loc['PTS'], 
                'QTR': live_info.iloc[index]['LIVE_PERIOD'], 
                'Time': live_info.iloc[index]['LIVE_PC_TIME'],
                'Status': live_info.iloc[index]['GAME_STATUS_TEXT']
                }
            index += 1
            # append each matchup to dataframe as a row, then fill nan values with 0's
            matchups_df = matchups_df.append(data, ignore_index=True)
            matchups_df = matchups_df.fillna(value=0)
        except:
            complete = True
        
    return matchups_df

# return current standings
# e_w optional (dont have to put anything)
#     defualt '' returns both in tuple (East Standings, West Standings)
#     if 'e' returns only east
#     if 'w' returns only west
def get_standings(e_w=''):
    # get data set from nba_api then choose the conference dataframes
    data_set = scoreboardv2.ScoreboardV2(day_offset=0, game_date=dt.datetime.now(), league_id='00')
    east_standings = data_set.east_conf_standings_by_day.get_data_frame()
    west_standings = data_set.west_conf_standings_by_day.get_data_frame()
    # drop useless
    east_standings = east_standings.drop(columns=['TEAM_ID', 'LEAGUE_ID', 'SEASON_ID'])
    west_standings = west_standings.drop(columns=['TEAM_ID', 'LEAGUE_ID', 'SEASON_ID'])
    if e_w == 'e': 
       return east_standings 
    if e_w == 'w':
        return west_standings
    return (east_standings, west_standings)


# week by week of 2021-22 season atm
def get_all_games():
    logs = teamgamelogs.TeamGameLogs(season_nullable='2021-22').get_data_frames()[0]
    df = pd.DataFrame(columns=['WEEK'])
    logs = logs.join(df)
    logs['WEEK'] = 0
    logs = logs.drop(columns=['SEASON_YEAR', 'TEAM_ABBREVIATION', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M',\
                            'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',\
                            'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS',\
                            'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK',\
                            'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK',\
                            'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK',\
                            'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK',\
                            'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK'])
    logs = logs[::-1]
    logs = logs.reset_index(drop='True')
    logs = logs.rename(columns={'TEAM_NAME':'TEAM_NAME1'})
    week_count = 1
    day_count = 0
    curr_start = logs['GAME_DATE'].iloc[0]
    curr_row_date = curr_start
    for i in range(len(logs)):
        curr_row_date = logs['GAME_DATE'].iloc[i]
        if curr_row_date == curr_start:
            logs['WEEK'].iloc[i] = week_count
        else:
            day_count += 1
            curr_start = logs['GAME_DATE'].iloc[i]
        if day_count == 7:
            day_count = 1
            week_count += 1
            logs['WEEK'].iloc[i] = week_count
        else:
            logs['WEEK'].iloc[i] = week_count
          
    return logs

# will retrieve upcoming week of games 
def get_upcoming_games():
    # not nba api but a nba json endpoint ig? if you click the link you will see
    data = requests.get("https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json")
    # format json for python
    data = data.json()
    # get todays date and format it to match what is expected in the json data
    date_today = dt.date.today()
    
    # get just the game information out of the json data response
    schedule = data.get('leagueSchedule').get('gameDates')
    # create dictionary of format {'game-date': gamesList}
    schedule_dict = {}
    for day in schedule:
        schedule_dict.update({f"{day.get('gameDate')}": day.get('games')})
    
    # create list of this weeks dates, in correct format
    this_week = []
    for i in range(7):
        next_day = date_today + dt.timedelta(days=i)
        next_day = next_day.strftime('%#m/%#d/%Y 12:00:00 AM')
        this_week.append(next_day)
    
    # create dict of this weeks games only
    upcoming_games = {}
    for day in this_week:
        upcoming_games.update({day: schedule_dict.get(day)})
    
    columns = ['Game_Date_Time', 'Home_Team', 'Home_Team_id', 'Home_Seed', 'Away_Team', 'Away_Team_id', 'Away_Seed',\
               'Matchup', 'Home_Pts', 'Away_Pts', 'Status', \
               'Game_Scoring_Leader', 'Game_Scoring_Leader_PTS']
    df = pd.DataFrame(columns=columns)
    
    for key in upcoming_games:
        game_list = upcoming_games.get(key)
        if game_list == None:
            continue
        for game in game_list:
            home_team = game.get('homeTeam')
            away_team = game.get('awayTeam')
            try:
                scoring_leader = game.get('pointsLeaders')[0]
            except:
                scoring_leader = {'firstName':'','lastName':'', 'points':0}
            date_time = dt.datetime.strptime(game.get('gameDateTimeEst'), '%Y-%m-%dT%H:%M:%SZ')
            date_time = date_time.strftime('%m/%d/%Y')
            insert = {
                'Game_Date_Time':date_time,
                'Day': game.get('day'),
                'Home_Team':f"{home_team.get('teamCity')} {home_team.get('teamName')}",
                'Home_Team_id':f"{home_team.get('teamId')}",
                'Home_Seed':home_team.get('seed'),
                'Away_Team':f"{away_team.get('teamCity')} {away_team.get('teamName')}",
                'Away_Team_id':f"{away_team.get('teamId')}",
                'Away_Seed':away_team.get('seed'),
                'Matchup':f"{away_team.get('teamTricode')} @ {home_team.get('teamTricode')}",
                'Home_Pts':home_team.get('score'),
                'Away_Pts':away_team.get('score'),
                'Status':game.get('gameStatusText'),
                'Game_Scoring_Leader':f"{scoring_leader.get('firstName')} {scoring_leader.get('lastName')}",
                'Game_Scoring_Leader_PTS': scoring_leader.get('points')
                }
            df = df.append(insert, ignore_index=True)
    return df
        
        
        
        
   