from msilib.schema import ListView
from datetime import datetime
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# from models in GoSports app directory
# this is how we access the db
from GoSports.models import Standings, Players, Teams, TeamSeasons, GamesThisWeek, PlayerSeasons, GamesToday


class HomePageView(TemplateView):
    template_name = "home.html"

class StandingsPageView(TemplateView):
    template_name = "standings.html"

class SchedulePageView(TemplateView):
    template_name = "schedule.html"

class TeamsPageView(TemplateView):
    template_name = "Teams.html"

class LoginPageView(TemplateView):
    template_name = "login.html"

class SignUpPageView(TemplateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class AccountCreated(TemplateView):
    template_name = "registration/created.html"

class DiscussionPageView(TemplateView):
    template_name = "discussion.html"

class SearchPageView(TemplateView):
    template_name = "search.html"

class DefaultTeamsPageView(TemplateView):
    template_name = "default_team.html"

# Create An Account Page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# The Standings Page
def standings_tables(request):
    # Standings returns the whole Standings Table
    # each row is an object .filter() allows us to search for rows by their value in the column given
    # in this case using conference
    # all fields available can be found in GoSports.models
    east = Standings.objects.filter(conference='East')
    west = Standings.objects.filter(conference='West')
    # returning a render (request given, template you want to use,
    # locals just referes to the local variables defined within this function
    # this makes it so you can access east and west within the html template!
    return render(request, 'standings.html', locals())

# An Individual Team Page
def team_page(request, team_name):
    # get team and their last five seasons
    team = Teams.objects.filter(name=team_name)[0]
    team_seasons = TeamSeasons.objects.filter(team=team)
    # get roster using team, then gather each players current szn
    # storing in dict {'Jayson Tatum': <PlayerSeason>}
    roster = Players.objects.filter(team_id=team)
    player_current_szns = {}
    for player in roster:
        # try expect catches players that dont have a szn
        try:
            recent_szn = PlayerSeasons.objects.filter(player=player, season_id='2021-22')[0]
            player_current_szns.update({player.full_name: recent_szn})
        except:
            pass
    return render(request, 'teams.html', locals())

# An Individual Player Page
def player_page(request, player_id=1):
    # Player stats for this season.
    player = Players.objects.filter(person_id=player_id)[0]
    player_szns = PlayerSeasons.objects.filter(player=player)

    team_name = f"{player.team_city} {player.team_name}"

    return render(request, 'players.html', locals())


def schedule_page(request):
    games_by_day = { }

    # Determine the next seven days of the week.
    standard_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    standard_day_keys = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    days = [ ] # next seven days of the week
    day_keys = [ ]
    today = datetime.today().weekday()
    
    for i in range(7):
        days.append( standard_days[ (today + i) % 7 ] )
        day_keys.append( standard_day_keys[ (today + i) % 7 ] )

    max_games = 0 # maximum number of games in one day (width of the schedule)

    for i in range(7):
        day = days[i]
        day_key = day_keys[i]

        games = GamesThisWeek.objects.filter(day=day_key)

        if ( len(games) > max_games ):
            max_games = len(games)

        games_by_day[ day ] = games

    num_cols = "a"*max_games

    return render(request, 'schedule.html', locals())


def search_page(request):
    model = Teams
    template_name = 'search_page.html'

    query = request.GET.get("search")
    teams = Teams.objects.filter (
        name__icontains=query
    )
    players = Players.objects.filter (
        full_name__icontains=query
    )
    return render(request, 'search.html', locals())

def home_page(request):
    games_today = GamesToday.objects.all()
    gameOver = GamesToday.objects.filter(status='final')
    return render(request, 'home.html', locals())
