# -*- coding: utf-8 -*-
"""
@author: Sam DeFrancisco

 *discarded* 
 
 not using this file really anymore, rather using Players_commons.py
 and Players_Seasons.py 
 
 not deleting incase need again
 
 *discarded*


 This file does most of the work in populating the mysql db
 Gathers each player from every rosters indivual stats reformatted into dataframes then entered into mysql db
 Gathers each teams total stats and enters them into sql db
 Uses team_player_api to gather stats
 
"""
# hopefull help for more stable connection
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



# pandas is used for its dataframes & series, helpful when putting data into sql database
import pandas as pd

# time is used to time.sleep() to avoid timeout in connection
import time 
import sqlite3

# different stuff used from the nba_api
# players and teams returns player and teams basic information
# the endpoints are used for different api calls to get stats and roster information
from nba_api.stats.static import teams

# files from backend directory
from gs_api.team_player_api import get_team_players_stats, team_season_stats
from gs_api.util import get_all_team_nameslist

player_stat_types = ['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
team_stat_types = ['TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'GP', 'WINS', 'LOSSES', 'WIN_PCT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES', 'CONF_COUNT', 'DIV_COUNT', 'NBA_FINALS_APPEARANCE', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PTS_RANK']


# main method runs at execution
def main():
    # connect to db
    conn = sqlite3.connect('gosports_nba_api.db')
    # list of generic team info, includes important column 'TEAM_ID' used to get specific returns from api
    # also grabbing list of just team names for league_team_stats df index
    all_teams = teams.get_teams()
    league_teams = get_all_team_nameslist(id_bool=False)
    team_df = pd.DataFrame(columns=player_stat_types)
    # Iterate through each team in the league
    # Get teams total stats as a team and append them to league_team_stats
    # Get each teams indivual roster stats, format into dict of form {'Team Name' : roster_stats_df}
    # Create sql table for roster and insert as 'Boston_Celtics'
    # special for loop stores idx as the count, and team as the objct within all_teams
    for idx, team in enumerate(all_teams):
        # store team id and name for convenience in f-strings
        currID = team['id']
        teamName = team['full_name']
        print(f"{teamName} Start ({idx+1}/{len(all_teams)})...\n")
        print("Gathering Roster Data..\n")
        # get roster stats
        stats = get_team_players_stats(currID)
        print("Finished..")
        time.sleep(1)
        
        #---------reformat dict and create sql table for team roster-----------#
        print('\tReformatting into team_dict and appending to Players')
        # get stats dict from above which is currently {'Jayson Tatum': pandas.series of stats, ... rest of team}
        team_dict = stats
        # convert dictkeys obj to a list for df index
        player_index = list(team_dict.keys())
        #team_df = pd.DataFrame(columns=player_stat_types, index=player_index)
        
        for player in player_index:
            player_stats = team_dict.get(player)
            try:
                team_df.loc[player] = player_stats.tolist()
            except Exception:
                # this exception is casued when player has no stats therefore an empty list []
                print(f"failed to add player to team_df, {player} has no stats, continuing...")
        # access dictionary by roster_stats['Boston Celtics']
        print('\tFinished')
    #-------------------------- End of Loop -----------------------------------------------#    
    
    # drop unneeded columns
    team_df = team_df.drop(columns=['LEAGUE_ID'])
    # drop any rows with nan values, gets rid of players with no 2021-2022 data
    team_df = team_df.dropna()
    # fix type for db again
    team_df[['GP','GS']] = team_df[['GP','GS']].astype('i')
    team_df['PLAYER_ID'] = team_df['PLAYER_ID'].astype('str')

    team_df.index.name = 'name'
    # send roster data frame to sql database, table called 'Team Name'
    team_df.to_sql(f"Players", con=conn, if_exists='replace')
    
    conn = conn.close()
    return
#----------------end of main()-------------------------------------#
   

if __name__=="__main__":
    main()

