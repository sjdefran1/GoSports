# -*- coding: utf-8 -*-
# Author - Sam DeFrancisco
"""
 Update mysql tables East_Standings West_Standings
 Update Games_Today table (scores, time left in games)
 My intention is for this to run often to keep website updated once integerated to db
 
"""

import sqlite3
import pandas as pd

# own api's from utils
from utils.game_api import games_today, get_standings

# populate nba_api_db
def main():
    # connect to mysql
    try:
        conn = sqlite3.connect('gosports_nba_api.db')
    except Exception as e:
        print('Unable to connect to nba_api_db\n\n')
        print(e)
   
    # get games today and create sql table
    print('Getting Games Today and updating sql tables...')
    game_today_ret = games_today()
    game_today_ret.to_sql('Games_Today', con=conn, if_exists='replace')
    print('Success\n')
    
    # get standings and create sql table for each
    print('Getting Standings and updating sql tables...')
    standings = get_standings()
    # combine east and west standings, rename index to rank and add 1 to each row so it doesnt start at 0
    standings_df = pd.concat(standings)
    standings_df.index.name = 'Rank'
    standings_df.index = standings_df.index + 1
    standings_df.to_sql('Standings', con=conn, if_exists='replace')
    print('Success\n')
    conn.close()

if __name__=="__main__":
    main()