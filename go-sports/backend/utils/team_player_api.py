# -*- coding: utf-8 -*-
"""
@author: Sam DeFrancisco

 This file incldues methods for finding team and player stats
 gets player info data, height weight etc
 roster statistics (each player indivual stats)
 most recent season stats for a player
 
"""



# used for time.sleep()
import time
# different stuff used from the nba_api
# players and teams returns player and teams basic information
# the endpoints are used for different api calls to get stats and roster information
from nba_api.stats.endpoints import commonplayerinfo, commonteamroster, playerprofilev2, teamyearbyyearstats
from nba_api.stats.static import teams

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



# function that gets player info data, height weight etc
def get_player_data(nba_player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=nba_player_id, headers=headers,timeout=100)
    df = player_info.common_player_info.get_data_frame()
    return df



# returns most recent season stats for a player
def player_recent_season_stats(playerID):
    gathered = False
    while gathered == False:
        try:
            player_stats = playerprofilev2.PlayerProfileV2(player_id=playerID, per_mode36='PerGame', timeout=10, headers=headers)
            gathered = True # got data
            player_stats = player_stats.season_totals_regular_season
            player_stats = player_stats.get_data_frame()
            # some players don't have 2021-2022 data, return as empty list
            if player_stats.empty == True:
                return []
            
            player_stats = player_stats.iloc[-1]
        # chooses last row of dataframe (most recent season)
        except:
            print('gather failed for player.. Sleeping for 5sec...Trying again')
            time.sleep(10)
    return player_stats

# returns roster statistics (each player indivual stats) for the team given by teamID
def get_team_players_stats(teamID):
    gathered = False
    while gathered == False:
        try:
            #get roster given by teamID so we have each players player_id
            roster_info = commonteamroster.CommonTeamRoster(team_id=teamID)
            gathered = True # data retrieved
            roster = roster_info.common_team_roster.get_data_frame()
            
            #store each players id into roster_players_ids
            # create roster_players = [(player id, 'full-name'), (player id, 'full-name'), ...]
            roster_players = []
            
            for i in range(0, len(roster)):
                roster_players.append([roster['PLAYER'][i], roster['PLAYER_ID'][i]])
            
            #iterate through each player in roster and append there stats to roster_dic as {'Player Name': pandas.series stats}
            roster_dic = {}
            for roster_player in roster_players:
                print(f"\t{roster_player[0]} Start..")
                # get stats for curr player
                # returned from player_recent_season_stats(), indexed @1 for player id rather than name
                player_stats = player_recent_season_stats(roster_player[1])
                roster_dic.update({f"{roster_player[0]}" : player_stats})
                time.sleep(.5)
                print(f"\t{roster_player[0]} Finished\n")
        except:
            print('team roster con failed, sleeping and trying again')
            time.sleep(10)
    return roster_dic

# returns 2021-2022 as a team data by teamID
def team_season_stats(teamID):
    # get data frames for yr by yr data, using teamID
    team_stats = teamyearbyyearstats.TeamYearByYearStats(team_id=teamID, per_mode_simple='PerGame')
    team_stats = team_stats.get_data_frames()[0]
    team_stats = team_stats.iloc[-1]
    return team_stats

def last_n_years(teamID, n):
    gathered = False
    while gathered == False:
        try:
            print(f"\t{teamID} Start...")
            team_log = teamyearbyyearstats.TeamYearByYearStats(team_id=teamID, per_mode_simple='PerGame', headers=headers, timeout=10)
            gathered = True # nice
            team_log = team_log.get_data_frames()[0]
            team_log = team_log[-n:]
            team_log = team_log.reset_index(drop=True)
            print(f"\t{teamID} Finished...")
        except:
            print('Game log retrieval error, sleeping and trying again')
            time.sleep(10)
    return team_log
# return each teams abr in a list
def get_all_abr():
    all_teams = teams.get_teams()
    all_abr = []
    for team in all_teams:
        all_abr.append(team.get('abbreviation'))
