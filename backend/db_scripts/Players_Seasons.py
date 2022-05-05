# -*- coding: utf-8 -*-
"""
@author: Sam DeFrancisco

Gathers all seasons for every player in Players table
Creates sql table PlayerSeasons

"""

# pandas is used for its dataframes & series, helpful when putting data into sql database
import pandas as pd

# time is used to time.sleep() to avoid timeout in connection
import time 
# conn
import sqlite3

# files from backend directory
from gs_api.team_player_api import get_team_players_stats
from gs_api.util import get_all_team_nameslist


def main():
    conn = sqlite3.connect('gosports_nba_api.db')
    teams = get_all_team_nameslist(id_bool=True)

    df = pd.DataFrame()
    for idx, team in enumerate(teams):
        print(f'{idx + 1}/{len(teams)} Starting {team[0]}...')
        insert = get_team_players_stats(teamID=team[1])
        df = df.append(insert)
        time.sleep(.6)
        print('Finished...\n')
    
    df = df.drop(columns=['LEAGUE_ID'])
    df = df.reset_index(drop=True)
    df.to_sql(name='PlayerSeasons', con=conn, if_exists='replace')
    return

    
if __name__ == '__main__':
    main()