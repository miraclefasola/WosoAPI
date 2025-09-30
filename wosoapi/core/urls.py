from django.urls import path, include
from core.views import *
import core.views as views


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "leagues/<str:league_code>/",
        LeagueSeasonDetailView.as_view(),
        name="club_stats_by_league",
    ),
    path(
        "clubs/<str:club_name>/",
        ClubSeasonStatView.as_view(),
        name="club_stats_by_club",
    ),
    path(
        "players/<str:player_id>/",
        PlayerSeasonDetailView.as_view(),
        name="player_detail",
    ),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
