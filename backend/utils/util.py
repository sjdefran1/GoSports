# -*- coding: utf-8 -*-
"""
@author: Sam DeFrancisco

 util holds useful functions that will be used over and over
 
"""
# different stuff used from the nba_api
# players and teams returns player and teams basic information
# the endpoints are used for different api calls to get stats and roster information
from nba_api.stats.static import teams

# returns dictionary w/ useful information for every team
def get_all_teams():
     return teams.get_teams()

# returns list where each element
# id_bool = True -> ('Team Name', 'Team_id')
# id_bool = False -> ('Team Name)
def get_all_team_nameslist(id_bool):
     if id_bool:
          league_teams = []
          all_teams = get_all_teams()
          for team in all_teams:
              league_teams.append((team['full_name'],  team['id']))
          return league_teams
     else:
          league_teams = []
          all_teams = get_all_teams()
          for team in all_teams:
              league_teams.append(team['full_name'])
          return league_teams
      
