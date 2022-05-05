# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 15:42:29 2022

@author: sjdef

Creates Players sql table
Includes name, playerid, & common info (height, pos, etc.)

"""

import pandas as pd
import time
import sqlite3

from gs_api.team_player_api import get_team_roster, get_player_common_info
from gs_api.util import get_all_team_nameslist


def main():
    conn = sqlite3.connect('gosports_nba_api.db')
    teams = get_all_team_nameslist(id_bool=True)
    # empty df to be appended to
    df = pd.DataFrame()
    # for each team get their roster
    # then gather basic info and append to dataframe
    for idx, team in enumerate(teams):
        print(f"({idx}/{len(teams)}) {team[0]} Start..")
        teamID = f"{team[1]}"
        roster = get_team_roster(teamID)
        for player in roster:
            print(f"\tStarting player {player}")
            # roster['Jayson Tatum'] -> '0230102'
            player_id = roster[player]
            player_info = get_player_common_info(player_id)
            df = df.append(player_info)
            time.sleep(.6)
            print('\tfinished\n')
        print(f"{team} Finished..")
    # create sql table
    df.to_sql(name="Players", con=conn, if_exists='replace')
    return

if __name__ == '__main__':
    main()