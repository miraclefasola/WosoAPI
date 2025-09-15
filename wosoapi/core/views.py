from django.shortcuts import render

from api.models import *
from django.views.generic import ListView, DetailView
from django_filters.rest_framework import filters, DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from itertools import groupby
from django.db.models import F


class HomeView(ListView):
    queryset = League.objects.all()
    template_name = "core/home.html"
    context_object_name = "leagues"


class ClubSeason(ListView):
    model = ClubSeasonStat
    template_name = "core/clubs.html"
    context_object_name = "clubs"

    def get_queryset(self):
        league_code = self.kwargs.get("league_code")
        self.league = get_object_or_404(League, code=league_code)
        queryset = ClubSeasonStat.objects.select_related(
            "club", "season", "league"
        ).filter(league=self.league)
        return queryset.order_by("league_position", "season__season", "club__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_qs = ClubSeasonStat.objects.select_related(
            "club", "season", "league"
        ).filter(league=self.league)
        distinct_qs = PlayerSeasonStats.objects.select_related(
            "club", "season", "player"
        ).filter(league=self.league)

        def get_season_key(obj):
            return obj.season.season

        def group_by_season(qs, order_by):
            ordered = qs.order_by("season__season", order_by)
            grouped = {}

            for season, obj in groupby(ordered, key=get_season_key):
                grouped[season] = list(obj)
            return grouped

        def group_by_distinct(qs, orderby):
            seasons = qs.values_list("season__season", flat=True).distinct()
            grouped = {}
            for season in seasons:
                season_players = qs.filter(season__season=season)

                top10 = season_players.order_by(orderby)[:10]
                grouped[season] = list(top10)
            return grouped

        goal_diff = base_qs.annotate(goal_diff=F("goals_scored") - F("goals_conceded"))

        context["season"] = Season.objects.all()
        context["club_names"] = Club.objects.all().distinct()
        context["goal_scored"] = group_by_season(base_qs, "-goals_scored")
        context["goal_conceded"] = group_by_season(base_qs, "-goals_conceded")
        context["xg_create"] = group_by_season(base_qs, "-xg_created")
        context["xg_concede"] = group_by_season(base_qs, "-xg_conceded")
        context["shot"] = group_by_season(base_qs, "-shots_allowed")
        context["shots_on_target"] = group_by_season(base_qs, "-shots_target_allowed")
        context["attempted_passes"] = group_by_season(
            base_qs, "-attempted_passes_against"
        )
        context["completed_passes"] = group_by_season(base_qs, "-comp_passes_allowed")
        context["passes_into_final_third"] = group_by_season(
            base_qs, "-passes_to_final_third_allowed"
        )
        context["passes_into_pen_area"] = group_by_season(
            base_qs, "-passes_to_pen_area_allowed"
        )
        context["league_table"] = group_by_season(goal_diff, "league_position")
        context["goal_difference"] = group_by_season(goal_diff, "goal_diff")
        context["player_minutes"] = group_by_distinct(distinct_qs, "-minutes_played")
        context["player_games_completed"] = group_by_distinct(
            distinct_qs, "-matches_completed"
        )
        context["player_matches_played"] = group_by_distinct(
            distinct_qs, "-matches_played"
        )
        context["player_minutes_played"] = group_by_distinct(
            distinct_qs, "-minutes_played"
        )
        context["player_matches_substituted"] = group_by_distinct(
            distinct_qs, "-matches_substituted"
        )
        context["player_unused_sub"] = group_by_distinct(distinct_qs, "-unused_sub")
        context["player_goals"] = group_by_distinct(distinct_qs, "-goals")
        context["player_assists"] = group_by_distinct(distinct_qs, "-assists")
        context["player_xg"] = group_by_distinct(distinct_qs, "-xg")
        context["player_npxg"] = group_by_distinct(distinct_qs, "-npxg")
        context["player_xg_performance"] = group_by_distinct(
            distinct_qs, "-xg_performance"
        )
        context["player_npxg_performance"] = group_by_distinct(
            distinct_qs, "-npxg_performance"
        )
        context["player_prog_carries"] = group_by_distinct(distinct_qs, "-prog_carries")
        context["player_prog_carries_final_3rd"] = group_by_distinct(
            distinct_qs, "-prog_carries_final_3rd"
        )
        context["player_prog_passes"] = group_by_distinct(distinct_qs, "-prog_passes")
        context["player_shots_target"] = group_by_distinct(distinct_qs, "-shots_target")
        context["player_passes_to_final_3rd"] = group_by_distinct(
            distinct_qs, "-passes_to_final_3rd"
        )
        context["player_passes_to_pen_area"] = group_by_distinct(
            distinct_qs, "-passes_to_pen_area"
        )
        context["player_pass_switches"] = group_by_distinct(
            distinct_qs, "-pass_switches"
        )
        context["player_through_ball"] = group_by_distinct(distinct_qs, "-through_ball")
        context["player_shots_creation_action"] = group_by_distinct(
            distinct_qs, "-shots_creation_action"
        )
        context["player_offsides"] = group_by_distinct(distinct_qs, "-offsides")
        context["player_pen_won"] = group_by_distinct(distinct_qs, "-pen_won")
        context["player_pen_conceded"] = group_by_distinct(distinct_qs, "-pen_conceded")
        context["player_tackles"] = group_by_distinct(distinct_qs, "-tackles")
        context["player_ball_recoveries"] = group_by_distinct(
            distinct_qs, "-ball_recoveries"
        )
        context["player_aerial_duels_won"] = group_by_distinct(
            distinct_qs, "-aerial_duels_won"
        )
        context["player_aerial_duels_lost"] = group_by_distinct(
            distinct_qs, "-aerial_duels_lost"
        )
        context["player_blocks"] = group_by_distinct(distinct_qs, "-blocks")
        context["player_tackles_won"] = group_by_distinct(distinct_qs, "-tackles_won")
        context["player_interceptions"] = group_by_distinct(
            distinct_qs, "-interceptions"
        )
        context["player_touches"] = group_by_distinct(distinct_qs, "-touches")
        context["player_dispossessed"] = group_by_distinct(distinct_qs, "-dispossessed")
        context["player_miscontrols"] = group_by_distinct(distinct_qs, "-miscontrols")
        context["player_take_ons"] = group_by_distinct(distinct_qs, "-take_ons")
        context["player_take_ons_won"] = group_by_distinct(distinct_qs, "-take_ons_won")
        context["player_fouls_won"] = group_by_distinct(distinct_qs, "-fouls_won")
        context["player_fouls_committed"] = group_by_distinct(
            distinct_qs, "-fouls_committed"
        )
        context["player_carries_to_final_3rd"] = group_by_distinct(
            distinct_qs, "-carries_to_final_3rd"
        )
        context["player_carries_to_pen_area"] = group_by_distinct(
            distinct_qs, "-carries_to_pen_area"
        )
        context["player_yellow_card"] = group_by_distinct(distinct_qs, "-yellow_card")
        context["player_red_card"] = group_by_distinct(distinct_qs, "-red_card")

        return context


class ClubSeasonStatView(ListView):
    model = ClubSeasonStat
    template_name = "core/clubstats.html"
    context_object_name = "clubs"

    def get_queryset(self):
        club_name = self.kwargs.get("club_name")
        self.club = get_object_or_404(Club, name=club_name)
        queryset = ClubSeasonStat.objects.select_related(
            "club", "season", "league"
        ).filter(club=self.club)
        return queryset.order_by("season__season", "club__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player_qs = PlayerSeasonStats.objects.select_related(
            "club", "season", "player"
        ).filter(club=self.club)
        goalkeeper_qs = Goalkeeper.objects.select_related(
            "player", "club", "season"
        ).filter(club=self.club)
        context["players"] = player_qs
        context["goalkeepers"] = goalkeeper_qs

        def get_season(obj):
            return obj.season.season

        def group_by_season(qs, orderby):
            ordered = qs.order_by("season__season", orderby)
            grouped = {}

            for season, obj in groupby(ordered, get_season):
                grouped[season] = list(obj)
            return grouped

        context["player_season"] = group_by_season(player_qs, "-position")
        context["goalkeeper_season"] = group_by_season(
            goalkeeper_qs, "player__full_name"
        )

        return context


class PlayerSeasonstatbyLeague(ListView):
    model = PlayerSeasonStats
    template_name = "core/playerstats.html"
    context_object_name = "players"

    def get_queryset(self):
        league_code = self.kwargs.get("league_code")
        self.league = get_object_or_404(League, code=league_code)
        queryset = ClubSeasonStat.objects.select_related(
            "club", "season", "league"
        ).filter(league=self.league)
        return queryset.order_by("league_position", "season__season", "club__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goalkeeper"] = Goalkeeper.objects.select_related(
            "player", "club", "season"
        ).filter(league=self.league)
        return context


class PlayerSeasonStatbyClub(ListView):
    model = PlayerSeasonStats
    template_name = "core/clubplayerstats.html"
    context_object_name = "players"

    def get_queryset(self):
        club_name = self.kwargs.get("club_name")
        self.club = get_object_or_404(Club, name=club_name)
        queryset = PlayerSeasonStats.objects.select_related(
            "player", "club", "season"
        ).filter(club=self.club)
        return queryset.order_by("-goals", "-assists", "player__full_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["goalkeeper"] = Goalkeeper.objects.select_related(
            "player", "club", "season"
        ).filter(club=self.club)
        return context
