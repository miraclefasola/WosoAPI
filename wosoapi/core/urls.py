from django.urls import path, include
from core.views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "leagues/<str:league_code>/", ClubSeason.as_view(), name="club_stats_by_league"
    ),
    path(
        "clubs/<str:club_name>/",
        ClubSeasonStatView.as_view(),
        name="club_stats_by_club",
    ),
    path(
        "player/league/<str:league_code>/",
        PlayerSeasonstatbyLeague.as_view(),
        name="player_season_stat_by_league",
    ),
    path(
        "players/<str:club_name>/",
        PlayerSeasonStatbyClub.as_view(),
        name="player_season_stat_by_club",
    ),
]
