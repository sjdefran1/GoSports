import pandas as pd
import time
import sqlite3

from utils.team_player_api import last_n_years
from utils.util import get_all_team_nameslist
team_stat_types = ['TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'GP', 'WINS', 'LOSSES', 'WIN_PCT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS',\
                   'PO_LOSSES', 'CONF_COUNT', 'DIV_COUNT', 'NBA_FINALS_APPEARANCE', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',\
                   'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PTS_RANK']

conn = sqlite3.connect('gosports_nba_api.db')
teams_list = get_all_team_nameslist(id_bool=True)

last_5_years = pd.DataFrame(columns=team_stat_types)

for team in teams_list:
    teams_lastn = last_n_years(team[1], 5)
    last_5_years = last_5_years.append(teams_lastn)
    time.sleep(.5)


last_5_years = last_5_years.drop(columns=['TEAM_CITY','TEAM_NAME','PO_WINS', 'PO_LOSSES', 'NBA_FINALS_APPEARANCE', 'PTS_RANK', 'CONF_COUNT', 'DIV_COUNT'])
last_5_years = last_5_years.dropna()
last_5_years[['TEAM_ID','GP','WINS','LOSSES','CONF_RANK', 'DIV_RANK']] = last_5_years[['TEAM_ID','GP','WINS','LOSSES','CONF_RANK', 'DIV_RANK']].astype('i')
last_5_years = last_5_years.reset_index(drop=True)
#league_team_stats.index.name = 'name'
last_5_years.to_sql('Seasons', con=conn, if_exists='replace')
