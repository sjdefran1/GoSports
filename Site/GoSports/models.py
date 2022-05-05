from tkinter import CASCADE
from django.db import models

#------------------------
# Using Django Models
#------------------------
# *** To mess around with models you can run in command line python manage.py shell in the Site directory
# this will give you an interactive python shell where you can import from GoSports.models to test things out****

# Example 1: Simple Calls
# -------------------------------------------- 
#     from GoSports.models import Teams
#     Teams.objects.all() -> Queryset of all teams
#     celts = Teams.objects.filter(name='Boston Celtics') -> <QuerySet [<Teams: Teams object (1610612738)>]> which is still a list
#
# - to get just the celtics object you can do
#     celts = Teams.objects.filter(name='Boston Celtics').first() ->  <Teams: Teams object (1610612738)>
#
# - you could then do
#     celts.name -> 'Boston Celtics'
#     celts.wins -> 50
#
# - loop through a set
#     for team in Teams.objects.all():
#         # team will be a row of the table
#         team.pts # can get its attrs
# 
# -------------------------------------------- 


# Example 2: Using DB Relations
# -------------------------------------------- 
# - Say you want all players on the celtics
#     from GoSports.models import Players, Teams
#     celts = Teams.objects.filter(name='Boston Celtics').first() 
#     celts_roster = Players.objects.filter(team=celts) ->   QuerySet [<Players: Players object (1628369)>, <Players: Players object (1627759)>, ... >]
#     for player in celts_roster:
#         player.name -> 'Jayson Tatum', 'Jaylen Brown', .....
# -------------------------------------------- 

# holds all teams as well as their ID
# PK: team_id
# FK: none
class Teams(models.Model):
    index = models.IntegerField(blank=True, null=True)
    name = models.TextField(db_column='TEAM_NAME', blank=True, null=True)  # 'Boston Celtics'
    team_id = models.IntegerField(primary_key=True, db_column='TEAM_ID', blank=True, null=False)  # '1610612737'
    color = models.TextField(db_column='TEAM_COLOR', blank=True, null=True)  # 'Boston Celtics'
    
    class Meta:
        managed = True
        db_table = 'Teams'

# holds each teams last 5 seaons stats
# PK: index
# FK: team, which allows you to get any teams last 5 seaons the same way as players
class TeamSeasons(models.Model):
    index = models.IntegerField(blank=True, null=False, primary_key=True)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)  
    year = models.TextField(db_column='YEAR', blank=True, null=True)  # '2017-18'
    gp = models.IntegerField(db_column='GP', blank=True, null=True)
    wins = models.IntegerField(db_column='WINS', blank=True, null=True)  
    losses = models.IntegerField(db_column='LOSSES', blank=True, null=True)
    win_pct = models.FloatField(db_column='WIN_PCT', blank=True, null=True)
    conf_rank = models.IntegerField(db_column='CONF_RANK', blank=True, null=True)
    div_rank = models.IntegerField(db_column='DIV_RANK', blank=True, null=True)
    fgm = models.FloatField(db_column='FGM', blank=True, null=True)
    fga = models.FloatField(db_column='FGA', blank=True, null=True)
    fg_pct = models.FloatField(db_column='FG_PCT', blank=True, null=True)
    fg3m = models.FloatField(db_column='FG3M', blank=True, null=True)
    fg3a = models.FloatField(db_column='FG3A', blank=True, null=True)
    fg3_pct = models.FloatField(db_column='FG3_PCT', blank=True, null=True)
    ftm = models.FloatField(db_column='FTM', blank=True, null=True)
    fta = models.FloatField(db_column='FTA', blank=True, null=True)
    ft_pct = models.FloatField(db_column='FT_PCT', blank=True, null=True)
    oreb = models.FloatField(db_column='OREB', blank=True, null=True) 
    dreb = models.FloatField(db_column='DREB', blank=True, null=True) 
    reb = models.FloatField(db_column='REB', blank=True, null=True) 
    ast = models.FloatField(db_column='AST', blank=True, null=True) 
    pf = models.FloatField(db_column='PF', blank=True, null=True)  
    stl = models.FloatField(db_column='STL', blank=True, null=True) 
    tov = models.FloatField(db_column='TOV', blank=True, null=True) 
    blk = models.FloatField(db_column='BLK', blank=True, null=True) 
    pts = models.FloatField(db_column='PTS', blank=True, null=True) 

    class Meta:
        managed = True
        db_table = 'TeamSeasons'


# Every Active player in the league
# Primary Key: player_id
# Foreign Key: team
# Comments on side for useful fields
class Players(models.Model):
    index = models.IntegerField(blank=True, null=True)
    person_id = models.IntegerField(db_column='PERSON_ID', primary_key=True, blank=True, null=False) 
    first_name = models.TextField(db_column='FIRST_NAME', blank=True, null=True)  
    last_name = models.TextField(db_column='LAST_NAME', blank=True, null=True)  
    full_name = models.TextField(db_column='DISPLAY_FIRST_LAST', blank=True, null=True)  # 'Jayson Tatum'
    display_last_comma_first = models.TextField(db_column='DISPLAY_LAST_COMMA_FIRST', blank=True, null=True)  # ignore
    display_fi_last = models.TextField(db_column='DISPLAY_FI_LAST', blank=True, null=True)  
    player_slug = models.TextField(db_column='PLAYER_SLUG', blank=True, null=True) 
    birthdate = models.TextField(db_column='BIRTHDATE', blank=True, null=True)  # '1992-04-26T00:00' weird format 
    school = models.TextField(db_column='SCHOOL', blank=True, null=True)  # 'Duke'
    country = models.TextField(db_column='COUNTRY', blank=True, null=True)  # 'USA'
    last_affiliation = models.TextField(db_column='LAST_AFFILIATION', blank=True, null=True)  
    height = models.TextField(db_column='HEIGHT', blank=True, null=True)  # '6-5'
    weight = models.TextField(db_column='WEIGHT', blank=True, null=True)  # 185
    season_exp = models.IntegerField(db_column='SEASON_EXP', blank=True, null=True)  # Seasons expierence, how many years in the league, 3
    jersey = models.TextField(db_column='JERSEY', blank=True, null=True)  # Jersey Num, 0
    position = models.TextField(db_column='POSITION', blank=True, null=True)  # Guard, Foward, Gaurd-Foward etc.
    rosterstatus = models.TextField(db_column='ROSTERSTATUS', blank=True, null=True)  # Only seems to be Active
    games_played_current_season_flag = models.TextField(db_column='GAMES_PLAYED_CURRENT_SEASON_FLAG', blank=True, null=True)  # ignore not useful
    team_id = models.ForeignKey(Teams, db_column='TEAM_ID', on_delete=models.CASCADE)  # team id '032030'
    team_name = models.TextField(db_column='TEAM_NAME', blank=True, null=True)  # 'Celtics'
    team_abbreviation = models.TextField(db_column='TEAM_ABBREVIATION', blank=True, null=True)  # 'BOS'
    team_code = models.TextField(db_column='TEAM_CODE', blank=True, null=True)  
    team_city = models.TextField(db_column='TEAM_CITY', blank=True, null=True)  # Boston
    playercode = models.TextField(db_column='PLAYERCODE', blank=True, null=True) 
    from_year = models.IntegerField(db_column='FROM_YEAR', blank=True, null=True)  # Last Season Played
    to_year = models.IntegerField(db_column='TO_YEAR', blank=True, null=True)  # First Szn Played
    dleague_flag = models.TextField(db_column='DLEAGUE_FLAG', blank=True, null=True) 
    nba_flag = models.TextField(db_column='NBA_FLAG', blank=True, null=True)  
    games_played_flag = models.TextField(db_column='GAMES_PLAYED_FLAG', blank=True, null=True)  
    draft_year = models.TextField(db_column='DRAFT_YEAR', blank=True, null=True)  # 2018
    draft_round = models.TextField(db_column='DRAFT_ROUND', blank=True, null=True)  # 1
    draft_number = models.TextField(db_column='DRAFT_NUMBER', blank=True, null=True)  # 3
    greatest_75_flag = models.TextField(db_column='GREATEST_75_FLAG', blank=True, null=True)  # If 'Y' Was on nba75, if 'N' was not on nba75
    full_team_name = f"{team_city} {team_name}"
    class Meta:
        managed = False
        db_table = 'Players'


class PlayerSeasons(models.Model):
    index = models.IntegerField(primary_key=True, blank=True, null=False)
    player = models.ForeignKey(Players, db_column='PLAYER_ID', on_delete=models.CASCADE)  # '0430430'
    season_id = models.TextField(db_column='SEASON_ID', blank=True, null=True)  # '2019-20'
    team_id = models.IntegerField(db_column='TEAM_ID', blank=True, null=True)  # '0320320'
    team_abbreviation = models.TextField(db_column='TEAM_ABBREVIATION', blank=True, null=True)  # 'BOS'
    player_age = models.FloatField(db_column='PLAYER_AGE', blank=True, null=True)  
    gp = models.IntegerField(db_column='GP', blank=True, null=True)  
    gs = models.IntegerField(db_column='GS', blank=True, null=True)  
    min = models.FloatField(db_column='MIN', blank=True, null=True)  
    fgm = models.FloatField(db_column='FGM', blank=True, null=True)  
    fga = models.FloatField(db_column='FGA', blank=True, null=True)  
    fg_pct = models.FloatField(db_column='FG_PCT', blank=True, null=True)  
    fg3m = models.FloatField(db_column='FG3M', blank=True, null=True)  
    fg3a = models.FloatField(db_column='FG3A', blank=True, null=True)  
    fg3_pct = models.FloatField(db_column='FG3_PCT', blank=True, null=True)  
    ftm = models.FloatField(db_column='FTM', blank=True, null=True)  
    fta = models.FloatField(db_column='FTA', blank=True, null=True)  
    ft_pct = models.FloatField(db_column='FT_PCT', blank=True, null=True)  
    oreb = models.FloatField(db_column='OREB', blank=True, null=True)  
    dreb = models.FloatField(db_column='DREB', blank=True, null=True)  
    reb = models.FloatField(db_column='REB', blank=True, null=True)  
    ast = models.FloatField(db_column='AST', blank=True, null=True)  
    stl = models.FloatField(db_column='STL', blank=True, null=True)  
    blk = models.FloatField(db_column='BLK', blank=True, null=True)  
    tov = models.FloatField(db_column='TOV', blank=True, null=True)  
    pf = models.FloatField(db_column='PF', blank=True, null=True)  
    pts = models.FloatField(db_column='PTS', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'PlayerSeasons'




# this currently holds all teams last 5 games played
# can find your teams last five using .filter(team_id=Team Object)
# Primary Key: index
# Foreign Key: team_id
class LastFiveGames(models.Model):
    index = models.IntegerField(primary_key = True, blank=True, null=False)
    team_id = models.ForeignKey(Teams, on_delete=models.CASCADE) # '1610612737' connects to Teams
    game_date = models.TextField(db_column='GAME_DATE', blank=True, null=True)  # 'APR 10, 2022'
    matchup = models.TextField(db_column='MATCHUP', blank=True, null=True) # 'ATL @ HOU' 
    wl = models.TextField(db_column='WL', blank=True, null=True)  # 'W' | 'L'
    w = models.IntegerField(db_column='W', blank=True, null=True)  
    l = models.IntegerField(db_column='L', blank=True, null=True)  
    w_pct = models.FloatField(db_column='W_PCT', blank=True, null=True)  
    min = models.IntegerField(db_column='MIN', blank=True, null=True)  
    fgm = models.IntegerField(db_column='FGM', blank=True, null=True)  
    fga = models.IntegerField(db_column='FGA', blank=True, null=True)  
    fg_pct = models.FloatField(db_column='FG_PCT', blank=True, null=True)  
    fg3m = models.IntegerField(db_column='FG3M', blank=True, null=True)  
    fg3a = models.IntegerField(db_column='FG3A', blank=True, null=True)  
    fg3_pct = models.FloatField(db_column='FG3_PCT', blank=True, null=True)  
    ftm = models.IntegerField(db_column='FTM', blank=True, null=True)  
    fta = models.IntegerField(db_column='FTA', blank=True, null=True)  
    ft_pct = models.FloatField(db_column='FT_PCT', blank=True, null=True)  
    oreb = models.IntegerField(db_column='OREB', blank=True, null=True)  
    dreb = models.IntegerField(db_column='DREB', blank=True, null=True)  
    reb = models.IntegerField(db_column='REB', blank=True, null=True)  
    ast = models.IntegerField(db_column='AST', blank=True, null=True)  
    stl = models.IntegerField(db_column='STL', blank=True, null=True)  
    blk = models.IntegerField(db_column='BLK', blank=True, null=True)  
    tov = models.IntegerField(db_column='TOV', blank=True, null=True)  
    pf = models.IntegerField(db_column='PF', blank=True, null=True)  
    pts = models.IntegerField(db_column='PTS', blank=True, null=True)  

    class Meta:
        managed = True
        db_table = 'LastFive'

# games this week for schedules tab  
#       
class GamesThisWeek(models.Model):
    index = models.IntegerField(primary_key=True, blank=True, null=False)
    game_date_time = models.TextField(db_column='Game_Date_Time', blank=True, null=True) # only game date, '04/15/2022' get time from status below
    home_team = models.TextField(db_column='Home_Team', blank=True, null=True)  # 'Boston Celtics'
    home_team_id = models.TextField(db_column='Home_Team_id', blank=True, null=True)  # '1610612738', currently not linked to teams, cant get django to have both home and way linked to there team
    home_seed = models.IntegerField(db_column='Home_Seed', blank=True, null=True)  # 2
    away_team = models.TextField(db_column='Away_Team', blank=True, null=True)   
    away_team_id = models.TextField(db_column='Away_Team_id', blank=True, null=True)
    away_seed = models.IntegerField(db_column='Away_Seed', blank=True, null=True)  
    matchup = models.TextField(db_column='Matchup', blank=True, null=True)  # 'BKN @ BOS'
    home_pts = models.IntegerField(db_column='Home_Pts', blank=True, null=True)  # 105
    away_pts = models.IntegerField(db_column='Away_Pts', blank=True, null=True)  
    status = models.TextField(db_column='Status', blank=True, null=True)  # '3:30 ET' | 'Final'
    game_scoring_leader = models.TextField(db_column='Game_Scoring_Leader', blank=True, null=True)  # 'Jayson Tatum'
    game_scoring_leader_pts = models.IntegerField(db_column='Game_Scoring_Leader_PTS', blank=True, null=True)  # 55
    day = models.TextField(db_column='Day', blank=True, null=True)  # 'Fri'

    class Meta:
        managed = True
        db_table = 'Games_This_Week'

# Games Today, live score and time
# PK: index
# FK:
class GamesToday(models.Model):
    index = models.IntegerField(blank=True, null=False, primary_key=True)
    home_team = models.TextField(db_column='Home_Team', blank=True, null=True)  # Field name made lowercase.
    home_id = models.IntegerField(db_column='Home_ID', blank=True, null=True)  # Field name made lowercase.
    away_team = models.TextField(db_column='Away_Team', blank=True, null=True)  # Field name made lowercase.
    away_id = models.IntegerField(db_column='Away_ID', blank=True, null=True)  # Field name made lowercase.
    home_pts = models.FloatField(db_column='Home_Pts', blank=True, null=True)  # Field name made lowercase.
    away_pts = models.FloatField(db_column='Away_Pts', blank=True, null=True)  # Field name made lowercase.
    qtr = models.IntegerField(db_column='QTR', blank=True, null=True)  # Field name made lowercase.
    time = models.TextField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Games_Today'

# This table holds all teams in the league
# get east / west using .filter(conference='East')
# PK: team
# FK: will be team_id in future, need to fix
class Standings(models.Model):
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # 1
    standingsdate = models.TextField(db_column='STANDINGSDATE', blank=True, null=True)  # '4/14/2022'
    conference = models.TextField(db_column='CONFERENCE', blank=True, null=True)  # 'East' | 'West'
    team = models.TextField(primary_key = True, db_column='TEAM', blank=True, null=False)  # 'Boston Celtics'
    g = models.IntegerField(db_column='G', blank=True, null=True)  # 72
    w = models.IntegerField(db_column='W', blank=True, null=True)  # 50
    l = models.IntegerField(db_column='L', blank=True, null=True)  # 22
    w_pct = models.FloatField(db_column='W_PCT', blank=True, null=True)  # .75
    home_record = models.TextField(db_column='HOME_RECORD', blank=True, null=True)  # '29-12'
    road_record = models.TextField(db_column='ROAD_RECORD', blank=True, null=True)  # '24-17'
    class Meta:
        managed = True
        db_table = 'Standings'

