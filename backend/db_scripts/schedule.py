import sqlite3
import pandas as pd

from gs_api.game_api import get_upcoming_games

import datetime

def main():
    conn = sqlite3.connect('gosports_nba_api.db')
    this_week = get_upcoming_games()
    this_week.to_sql(name='Games_This_Week', con=conn, if_exists='replace')


if __name__ == "__main__":
    main()
