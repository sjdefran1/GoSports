from msilib.schema import ListView
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
from GoSports.models import Standings, Players, Teams, Seasons, GamesThisWeek


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
    team = Teams.objects.filter(name=team_name)[0]
    seasons = Seasons.objects.filter(team=team)

    roster = Players.objects.filter(team_id=team.team_id)

    return render(request, 'teams.html', locals())

# An Individual Player Page
def player_page(request, player_id=1):
    # Player stats for this season.
    player = Players.objects.filter(player_id=player_id)[0]

    team_name = Teams.objects.filter(team_id=player.team_id)[0].name

    return render(request, 'players.html', locals())

def schedule_page(request):
    gameslist = {
        'Mon':GamesThisWeek.objects.filter(day='Mon'),
        'Tue':GamesThisWeek.objects.filter(day='Tue'),
        'Wed':GamesThisWeek.objects.filter(day='Wed'),
        'Thu':GamesThisWeek.objects.filter(day='Thu'),
        'Fri':GamesThisWeek.objects.filter(day='Fri'),
        'Sat':GamesThisWeek.objects.filter(day='Sat'),
        'Sun':GamesThisWeek.objects.filter(day='Sun')
    }

    return render(request, 'schedule.html', locals())
def search_page(request):
    model = Teams
    template_name = 'search_page.html'
    queryset = Teams.objects.filter(name='Boston Celtics')

    query = request.GET.get("search")
    object_list = Teams.objects.filter (
        name__icontains=query
    )
    return render(request, 'search.html', locals())
