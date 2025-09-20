from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"countries", CountryView, basename="all_countries")
router.register(r"leagues", LeagueView, basename="all_leagues")
router.register(r"seasons", SeasonView, basename="seasons")
router.register(r"clubs", Clubview, basename="all_clubs")
router.register(r"clubstats", ClubSeasonStatView, basename="club_stats")
router.register(r"players", PlayerView, basename="all_players")
router.register(r"playerstats", PlayerSeasonStatsView, basename="season_player_stats")
router.register(r"goalkeepers", GoalkeeperView, basename="goalkeepers")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "leagues/<int:league_id>/seasons/",
        LeagueSeasonView.as_view(),
        name="league_seasons",
    ),
    # Returns all seasons that belong to a specific league (by league_id)
    path(
        "leagues/<int:league_id>/clubs/", LeagueClubView.as_view(), name="league_clubs"
    ),
    # Returns all clubs that play in a specific league (by league_id)
    path(
        "leagues/<int:league_id>/players/",
        LeaguePlayerView.as_view(),
        name="league_players",
    ),
    #  Returns all players that belong to clubs in a specific league (by league_id)
    path(
        "leagues/<int:league_id>/goalkeepers/",
        LeagueGoalkeeperView.as_view(),
        name="league_goalkeepers",
    ),
    #  Returns all goalkeepers that belong to clubs in a specific league (by league_id)
    # ---- Club nested routes ----
    path("clubs/<int:club_id>/", ClubDetailView.as_view(), name="club_detail"),
    #  Returns details + stats for a specific club (by club_id)
    path("clubs/<int:club_id>/players/", ClubPlayerView.as_view(), name="club_players"),
    #  Returns all players (with stats) that belong to a specific club (by club_id)
    path(
        "clubs/<int:club_id>/goalkeepers/",
        ClubGoalkeeperView.as_view(),
        name="club_goalkeepers",
    ),
    path("/documentation", HomeView.as_view(), name="documentation_view"),
    #  Returns all goalkeepers (with stats) that belong to a specific club (by club_id)
]
