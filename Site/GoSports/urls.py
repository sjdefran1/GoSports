from django.urls import path
from .views import HomePageView, SearchPageView, SchedulePageView, LoginPageView, DiscussionPageView, AccountCreated, home_page, signup, standings_tables, player_page, team_page, search_page, schedule_page, DefaultTeamsPageView, choose_team_page

urlpatterns = [
    path("", home_page, name="home"),
    path("standings/", standings_tables, name="standings"),
    path("schedule/", schedule_page, name="schedule"),
    path("login/", LoginPageView.as_view(), name="login"),
    path("accounts/signup/", signup, name="signup"),
    path("accounts/created/", AccountCreated.as_view() , name="accounts_created"),
    path("discussion/", DiscussionPageView.as_view(), name="discussion"),
    path("teams/", choose_team_page, name="teams"),
    path("team/<str:team_name>/", team_page, name="team"),
    path("players/<int:player_id>/",  player_page , name="players"),
    path("search/", search_page, name="search")
]