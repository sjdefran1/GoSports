# -*- coding: utf-8 -*-
"""
@author: Sam DeFrancisco

  Used to further populate nba_api_db
  creates last five table for each team
  
"""
import sqlite3
# time.sleep()
import time
import pandas as pd

# own api's
from utils.util import get_all_team_nameslist
from utils.game_api import last_n_games
# finding teams by id
from nba_api.stats.static import teams

# populate nba_api_db
def main():
    # connect to mysql
    try:
        conn = sqlite3.connect('gosports_nba_api.db')
    except Exception as e:
        print('Unable to connect to nba_api_db\n\n')
        print(e)
   
    # get all teams, ('Team Name', 'Team_id')
    all_teams = get_all_team_nameslist(id_bool=True)
    # get each teams last 5 games
    print('Getting Last 5 games for each team and updating tables...\n')
    game_logs = pd.DataFrame()
    for team in all_teams:
        game_logs = game_logs.append(last_n_games(team[1], n=5))
        time.sleep(.8)

    game_logs = game_logs.drop(columns='Game_ID')
    game_logs = game_logs.dropna()
    game_logs = game_logs.reset_index(drop='True')
    game_logs.to_sql('LastFive', con=conn, if_exists='replace')
    print('Success')
    conn = conn.close()
    
if __name__=="__main__":
    main()

