"""
@author Sam DeFrancisco
This file creates the Teams table in sqlite db
will hold (team name, teamid)

"""


# pandas is used for its dataframes & series, helpful when putting data into sql database
import pandas as pd
import json

# time is used to time.sleep() to avoid timeout in connection
import time 
import sqlite3

from gs_api.util import get_all_team_nameslist
from gs_api.team_player_api import get_color

def main():
    conn = sqlite3.connect('gosports_nba_api.db')
    teams_list = get_all_team_nameslist(id_bool=True)
    teams_df = pd.DataFrame(columns=['TEAM_NAME', 'TEAM_ID', 'TEAM_COLOR'])
    f = open('colors.json')
    colors = json.load(f)
    
    for team in teams_list:
        color = colors.get(f"{team[1]}")
        teams_df = teams_df.append({'TEAM_NAME': team[0], 'TEAM_ID':team[1], 'TEAM_COLOR': color}, ignore_index=True)

    teams_df.to_sql(name='Teams',con=conn, if_exists='replace')
    return

if __name__=="__main__":
    main()