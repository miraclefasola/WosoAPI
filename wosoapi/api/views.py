from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from api.serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.permissions import IsSuperUserOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import filters, DjangoFilterBackend
from rest_framework import filters
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "api/documentation.html"


class CountryView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    authentication_classes = [JWTAuthentication]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "name", "code"]
    search_fields = ["id", "name", "code"]
    ordering = ["name"]
    filterset_fields = {
        "id": ["exact"],
        "name": ["exact", "icontains"],
        "code": ["exact"],
    }


class LeagueView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = LeagueSerializer
    queryset = League.objects.select_related("country").all()
    authentication_classes = [JWTAuthentication]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "name", "country__name", "code", "total_clubs"]
    search_fields = ["id", "name", "country__name", "code", "total_clubs"]
    ordering = ["name"]
    filterset_fields = {
        "id": ["exact"],
        "name": ["exact", "icontains"],
        "country__name": ["exact", "icontains"],
        "code": ["exact"],
        "total_clubs": ["exact", "gte", "lte", "range"],
    }


class SeasonView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Season.objects.select_related("league").all()
    serializer_class = SeasonSerializer

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "season", "league__name"]
    search_fields = ["id", "season", "league__name"]
    ordering = ["season", "league__name"]
    filterset_fields = {
        "id": ["exact"],
        "season": ["exact"],
        "league__name": ["exact", "icontains"],
    }


class Clubview(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ClubSerializer
    queryset = Club.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "name", "fbref_id", "stadium"]
    search_fields = ["id", "name", "fbref_id", "stadium"]
    ordering = ["name", "fbref_id"]
    filterset_fields = {
        "id": ["exact"],
        "name": ["exact", "icontains"],
        "fbref_id": ["exact"],
        "stadium": ["exact", "icontains"],
    }


class ClubSeasonStatView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = ClubSeasonStat.objects.select_related("club", "season", "league").all()
    serializer_class = ClubSeasonStatSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "id",
        "club__name",
        "season__season",
        "league__name",
        "points_won",
        "league_position",
        "matches_played",
        "win",
        "draw",
        "lost",
        "goals_scored",
        "goals_conceded",
        "xg_created",
        "xg_conceded",
        "shots_allowed",
        "shots_target_allowed",
        "attempted_passes_against",
        "comp_passes_allowed",
        "passes_to_final_third_allowed",
        "passes_to_pen_area_allowed",
    ]
    search_fields = [
        "id",
        "club__name",
        "season__season",
        "league__name",
        "points_won",
        "league_position",
        "matches_played",
        "win",
        "draw",
        "lost",
        "goals_scored",
        "goals_conceded",
        "xg_created",
        "xg_conceded",
        "shots_allowed",
        "shots_target_allowed",
        "attempted_passes_against",
        "comp_passes_allowed",
        "passes_to_final_third_allowed",
        "passes_to_pen_area_allowed",
    ]
    ordering = ["league_position"]
    filterset_fields = {
        "id": ["exact"],
        "club__name": ["exact", "icontains"],
        "season__season": ["exact"],
        "league__name": ["exact", "icontains"],
        "points_won": ["exact", "gte", "lte", "range"],
        "league_position": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "win": ["exact", "gte", "lte", "range"],
        "draw": ["exact", "gte", "lte", "range"],
        "lost": ["exact", "gte", "lte", "range"],
        "goals_scored": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "xg_created": ["exact", "gte", "lte", "range"],
        "xg_conceded": ["exact", "gte", "lte", "range"],
        "shots_allowed": ["exact", "gte", "lte", "range"],
        "shots_target_allowed": ["exact", "gte", "lte", "range"],
        "attempted_passes_against": ["exact", "gte", "lte", "range"],
        "comp_passes_allowed": ["exact", "gte", "lte", "range"],
        "passes_to_final_third_allowed": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area_allowed": ["exact", "gte", "lte", "range"],
    }


class PlayerView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "full_name", "fbref_id", "nationality", "age"]
    search_fields = ["id", "full_name", "fbref_id", "nationality", "age"]
    ordering = ["full_name"]
    filterset_fields = {
        "id": ["exact"],
        "full_name": ["exact", "icontains"],
        "fbref_id": ["exact"],
        "nationality": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
    }


class PlayerSeasonStatsView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = PlayerSeasonStats.objects.select_related(
        "player", "club", "league", "season"
    ).all()
    serializer_class = PlayerSeasonStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "id",
        "fouls_committed",
        "fouls_won",
        "player__full_name",
        "club__name",
        "league__code",
        "league__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "matches_completed",
        "matches_substituted",
        "unused_sub",
        "goals",
        "assists",
        "xg",
        "npxg",
        "xg_performance",
        "npxg_performance",
        "prog_carries",
        "prog_carries_final_3rd",
        "prog_passes",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "pass_switches",
        "through_ball",
        "shots_creation_action",
        "offsides",
        "pen_won",
        "pen_conceded",
        "tackles",
        "tackles_won",
        "interceptions",
        "ball_recoveries",
        "aerial_duels_won",
        "aerial_duels_lost",
        "blocks",
        "touches",
        "dispossessed",
        "miscontrols",
        "take_ons",
        "take_ons_won" "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    search_fields = [
        "id",
        "fouls_committed",
        "fouls_won",
        "player__full_name",
        "club__name",
        "league__code",
        "league__name" "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "matches_completed",
        "matches_substituted",
        "unused_sub",
        "goals",
        "assists",
        "xg",
        "npxg",
        "xg_performance",
        "npxg_performance",
        "prog_carries",
        "prog_carries_final_3rd",
        "prog_passes",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "pass_switches",
        "through_ball",
        "shots_creation_action",
        "offsides",
        "pen_won",
        "pen_conceded",
        "tackles",
        "tackles_won",
        "interceptions",
        "ball_recoveries",
        "aerial_duels_won",
        "aerial_duels_lost",
        "blocks",
        "touches",
        "dispossessed",
        "miscontrols",
        "take_ons",
        "take_ons_won" "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    ordering = ["-goals", "-assists", "-minutes_played", "player__full_name"]
    filterset_fields = {
        "id": ["exact"],
        "fouls_committed": ["exact", "gte", "lte", "range"],
        "fouls_won": ["exact", "gte", "lte", "range"],
        "player__full_name": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
        "league__code": ["exact"],
        "league__name": ["exact"],
        "season__season": ["exact"],
        "position": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "matches_completed": ["exact", "gte", "lte", "range"],
        "matches_substituted": ["exact", "gte", "lte", "range"],
        "unused_sub": ["exact", "gte", "lte", "range"],
        "goals": ["exact", "gte", "lte", "range"],
        "assists": ["exact", "gte", "lte", "range"],
        "xg": ["exact", "gte", "lte", "range"],
        "npxg": ["exact", "gte", "lte", "range"],
        "xg_performance": ["exact", "gte", "lte", "range"],
        "npxg_performance": ["exact", "gte", "lte", "range"],
        "prog_carries": ["exact", "gte", "lte", "range"],
        "prog_carries_final_3rd": ["exact", "gte", "lte", "range"],
        "prog_passes": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes_to_final_3rd": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
        "pass_switches": ["exact", "gte", "lte", "range"],
        "through_ball": ["exact", "gte", "lte", "range"],
        "shots_creation_action": ["exact", "gte", "lte", "range"],
        "offsides": ["exact", "gte", "lte", "range"],
        "pen_won": ["exact", "gte", "lte", "range"],
        "pen_conceded": ["exact", "gte", "lte", "range"],
        "tackles": ["exact", "gte", "lte", "range"],
        "tackles_won": ["exact", "gte", "lte", "range"],
        "interceptions": ["exact", "gte", "lte", "range"],
        "ball_recoveries": ["exact", "gte", "lte", "range"],
        "aerial_duels_won": ["exact", "gte", "lte", "range"],
        "aerial_duels_lost": ["exact", "gte", "lte", "range"],
        "blocks": ["exact", "gte", "lte", "range"],
        "touches": ["exact", "gte", "lte", "range"],
        "dispossessed": ["exact", "gte", "lte", "range"],
        "miscontrols": ["exact", "gte", "lte", "range"],
        "take_ons": ["exact", "gte", "lte", "range"],
        "take_ons_won": ["exact", "gte", "lte", "range"],
        "carries_to_final_3rd": ["exact", "gte", "lte", "range"],
        "carries_to_pen_area": ["exact", "gte", "lte", "range"],
        "yellow_card": ["exact", "gte", "lte", "range"],
        "red_card": ["exact", "gte", "lte", "range"],
    }


class GoalkeeperView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Goalkeeper.objects.select_related(
        "player", "club", "league", "season"
    ).all()
    serializer_class = GoalkeeperSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "player__full_name",
        "club__name",
        "league__code",
        "league__name",
        "season__season",
        "age",
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "shots_faced",
        "saves",
        "save_percentage",
        "clean_sheets",
        "psxg",
        "psxg_performance",
        "pen_saved",
        "passes",
        "crosses_stopped",
        "sweeper_action",
        "sweeper_action_per90",
    ]
    search_fields = [
        "player__full_name",
        "club__name",
        "league__code",
        "league__name",
        "season__season",
        "age",
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "shots_faced",
        "saves",
        "save_percentage",
        "clean_sheets",
        "psxg",
        "psxg_performance",
        "pen_saved",
        "passes",
        "crosses_stopped",
        "sweeper_action",
        "sweeper_action_per90",
    ]
    ordering = [
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "player__full_name",
    ]
    filterset_fields = {
        "player__full_name": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
        "league__code": ["exact"],
        "league__name": ["exact"],
        "season__season": ["exact"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "shots_faced": ["exact", "gte", "lte", "range"],
        "saves": ["exact", "gte", "lte", "range"],
        "save_percentage": ["exact", "gte", "lte", "range"],
        "clean_sheets": ["exact", "gte", "lte", "range"],
        "psxg": ["exact", "gte", "lte", "range"],
        "psxg_performance": ["exact", "gte", "lte", "range"],
        "pen_saved": ["exact", "gte", "lte", "range"],
        "passes": ["exact", "gte", "lte", "range"],
        "crosses_stopped": ["exact", "gte", "lte", "range"],
        "sweeper_action": ["exact", "gte", "lte", "range"],
        "sweeper_action_per90": ["exact", "gte", "lte", "range"],
    }


class LeagueSeasonView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = SeasonSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "season", "league__name"]
    search_fields = ["id", "season", "league__name"]
    ordering = ["season", "league__name"]
    filterset_fields = {
        "id": ["exact"],
        "season": ["exact"],
        "league__name": ["exact", "icontains"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Season.objects.select_related("league").filter(league_id=league_id)
        return queryset


class LeagueClubView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ClubSeasonStatSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "name", "fbref_id", "league__name"]
    search_fields = ["id", "name", "fbref_id", "league__name"]
    ordering = ["name", "fbref_id"]
    filterset_fields = {
        "id": ["exact"],
        "name": ["exact", "icontains"],
        "fbref_id": ["exact"],
        "league__name": ["exact", "icontains"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = ClubSeasonStat.objects.select_related(
            "club", "league", "season"
        ).filter(league_id=league_id)
        return queryset


class LeaguePlayerView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSeasonStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "id",
        "fouls_committed",
        "fouls_won",
        "player__full_name",
        "club__name",
        "league__code",
        "league__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "matches_completed",
        "matches_substituted",
        "unused_sub",
        "goals",
        "assists",
        "xg",
        "npxg",
        "xg_performance",
        "npxg_performance",
        "prog_carries",
        "prog_carries_final_3rd",
        "prog_passes",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "pass_switches",
        "through_ball",
        "shots_creation_action",
        "offsides",
        "pen_won",
        "pen_conceded",
        "tackles",
        "tackles_won",
        "interceptions",
        "ball_recoveries",
        "aerial_duels_won",
        "aerial_duels_lost",
        "blocks",
        "touches",
        "dispossessed",
        "miscontrols",
        "take_ons",
        "take_ons_won" "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    search_fields = [
        "id",
        "fouls_committed",
        "fouls_won",
        "player__full_name",
        "club__name",
        "league__code",
        "league__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "matches_completed",
        "matches_substituted",
        "unused_sub",
        "goals",
        "assists",
        "xg",
        "npxg",
        "xg_performance",
        "npxg_performance",
        "prog_carries",
        "prog_carries_final_3rd",
        "prog_passes",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "pass_switches",
        "through_ball",
        "shots_creation_action",
        "offsides",
        "pen_won",
        "pen_conceded",
        "tackles",
        "tackles_won",
        "interceptions",
        "ball_recoveries",
        "aerial_duels_won",
        "aerial_duels_lost",
        "blocks",
        "touches",
        "dispossessed",
        "miscontrols",
        "take_ons",
        "take_ons_won" "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    ordering = ["player__full_name", "player__fbref_id"]
    filterset_fields = {
        "id": ["exact"],
        "fouls_committed": ["exact", "gte", "lte", "range"],
        "fouls_won": ["exact", "gte", "lte", "range"],
        "player__full_name": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
        "league__code": ["exact"],
        "league__name": ["exact"],
        "season__season": ["exact"],
        "position": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "matches_completed": ["exact", "gte", "lte", "range"],
        "matches_substituted": ["exact", "gte", "lte", "range"],
        "unused_sub": ["exact", "gte", "lte", "range"],
        "goals": ["exact", "gte", "lte", "range"],
        "assists": ["exact", "gte", "lte", "range"],
        "xg": ["exact", "gte", "lte", "range"],
        "npxg": ["exact", "gte", "lte", "range"],
        "xg_performance": ["exact", "gte", "lte", "range"],
        "npxg_performance": ["exact", "gte", "lte", "range"],
        "prog_carrides": ["exact", "gte", "lte", "range"],
        "prog_carries_final_3rd": ["exact", "gte", "lte", "range"],
        "prog_passes": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes_to_final_3rd": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
        "pass_switches": ["exact", "gte", "lte", "range"],
        "through_ball": ["exact", "gte", "lte", "range"],
        "shots_creation_action": ["exact", "gte", "lte", "range"],
        "offsides": ["exact", "gte", "lte", "range"],
        "pen_won": ["exact", "gte", "lte", "range"],
        "pen_conceded": ["exact", "gte", "lte", "range"],
        "tackles": ["exact", "gte", "lte", "range"],
        "tackles_won": ["exact", "gte", "lte", "range"],
        "interceptions": ["exact", "gte", "lte", "range"],
        "ball_recoveries": ["exact", "gte", "lte", "range"],
        "aerial_duels_won": ["exact", "gte", "lte", "range"],
        "aerial_duels_lost": ["exact", "gte", "lte", "range"],
        "blocks": ["exact", "gte", "lte", "range"],
        "touches": ["exact", "gte", "lte", "range"],
        "dispossessed": ["exact", "gte", "lte", "range"],
        "miscontrols": ["exact", "gte", "lte", "range"],
        "take_ons": ["exact", "gte", "lte", "range"],
        "take_ons_won": ["exact", "gte", "lte", "range"],
        "carries_to_final_3rd": ["exact", "gte", "lte", "range"],
        "carries_to_pen_area": ["exact", "gte", "lte", "range"],
        "yellow_card": ["exact", "gte", "lte", "range"],
        "red_card": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = PlayerSeasonStats.objects.select_related(
            "player", "club", "season"
        ).filter(club__league_id=league_id)
        return queryset


class LeagueGoalkeeperView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = GoalkeeperSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "player__full_name",
        "club__name",
        "season__season",
        "age",
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "shots_faced",
        "saves",
        "save_percentage",
        "clean_sheets",
        "psxg",
        "psxg_performance",
        "pen_saved",
        "passes",
        "crosses_stopped",
        "sweeper_action",
        "sweeper_action_per90",
    ]
    search_fields = [
        "player__full_name",
        "club__name",
        "season__season",
        "age",
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "shots_faced",
        "saves",
        "save_percentage",
        "clean_sheets",
        "psxg",
        "psxg_performance",
        "pen_saved",
        "passes",
        "crosses_stopped",
        "sweeper_action",
        "sweeper_action_per90",
    ]
    ordering = [
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "psxg",
        "player__full_name",
    ]
    filterset_fields = {
        "player__full_name": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
        "league__code": ["exact"],
        "league__name": ["exact"],
        "season__season": ["exact"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "shots_faced": ["exact", "gte", "lte", "range"],
        "saves": ["exact", "gte", "lte", "range"],
        "save_percentage": ["exact", "gte", "lte", "range"],
        "clean_sheets": ["exact", "gte", "lte", "range"],
        "psxg": ["exact", "gte", "lte", "range"],
        "psxg_performance": ["exact", "gte", "lte", "range"],
        "pen_saved": ["exact", "gte", "lte", "range"],
        "passes": ["exact", "gte", "lte", "range"],
        "crosses_stopped": ["exact", "gte", "lte", "range"],
        "sweeper_action": ["exact", "gte", "lte", "range"],
        "sweeper_action_per90": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Goalkeeper.objects.select_related(
            "player", "league", "club", "season"
        ).filter(league_id=league_id)
        return queryset


class ClubDetailView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ClubSeasonStatSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "id",
        "club__name",
        "season__season",
        "points_won",
        "league_position",
        "matches_played",
        "win",
        "draw",
        "lost",
        "goals_scored",
        "goals_conceded",
        "xg_created",
        "xg_conceded",
        "shots_allowed",
        "shots_target_allowed",
        "attempted_passes_against",
        "comp_passes_allowed",
        "passes_to_final_third_allowed",
        "passes_to_pen_area_allowed",
    ]
    search_fields = [
        "id",
        "club__name",
        "season__season",
        "points_won",
        "league_position",
        "matches_played",
        "win",
        "draw",
        "lost",
        "goals_scored",
        "goals_conceded",
        "xg_created",
        "xg_conceded",
        "shots_allowed",
        "shots_target_allowed",
        "attempted_passes_against",
        "comp_passes_allowed",
        "passes_to_final_third_allowed",
        "passes_to_pen_area_allowed",
    ]
    ordering = ["league_position"]
    filterset_fields = {
        "id": ["exact"],
        "club__name": ["exact", "icontains"],
        "season__season": ["exact"],
        "points_won": ["exact", "gte", "lte", "range"],
        "league_position": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "win": ["exact", "gte", "lte", "range"],
        "draw": ["exact", "gte", "lte", "range"],
        "lost": ["exact", "gte", "lte", "range"],
        "goals_scored": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "xg_created": ["exact", "gte", "lte", "range"],
        "xg_conceded": ["exact", "gte", "lte", "range"],
        "shots_allowed": ["exact", "gte", "lte", "range"],
        "shots_target_allowed": ["exact", "gte", "lte", "range"],
        "attempted_passes_against": ["exact", "gte", "lte", "range"],
        "comp_passes_allowed": ["exact", "gte", "lte", "range"],
        "passes_to_final_third_allowed": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area_allowed": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = ClubSeasonStat.objects.select_related("club", "season").filter(
            club_id=club_id
        )
        return queryset


class ClubPlayerView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSeasonStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "id",
        "fouls_committed",
        "fouls_won",
        "player__full_name",
        "club__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "matches_completed",
        "matches_substituted",
        "unused_sub",
        "goals",
        "assists",
        "xg",
        "npxg",
        "xg_performance",
        "npxg_performance",
        "prog_carries",
        "prog_carries_final_3rd",
        "prog_passes",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "pass_switches",
        "through_ball",
        "shots_creation_action",
        "offsides",
        "pen_won",
        "pen_conceded",
        "tackles",
        "tackles_won",
        "interceptions",
        "ball_recoveries",
        "aerial_duels_won",
        "aerial_duels_lost",
        "blocks",
        "touches",
        "dispossessed",
        "miscontrols",
        "take_ons",
        "take_ons_won" "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    search_fields = [
        "id",
        "fouls_committed",
        "fouls_won",
        "player__full_name",
        "club__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "matches_completed",
        "matches_substituted",
        "unused_sub",
        "goals",
        "assists",
        "xg",
        "npxg",
        "xg_performance",
        "npxg_performance",
        "prog_carries",
        "prog_carries_final_3rd",
        "prog_passes",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "pass_switches",
        "through_ball",
        "shots_creation_action",
        "offsides",
        "pen_won",
        "pen_conceded",
        "tackles",
        "tackles_won",
        "interceptions",
        "ball_recoveries",
        "aerial_duels_won",
        "aerial_duels_lost",
        "blocks",
        "touches",
        "dispossessed",
        "miscontrols",
        "take_ons",
        "take_ons_won" "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    ordering = ["-goals", "-assists", "-minutes_played", "player__full_name"]
    filterset_fields = {
        "id": ["exact"],
        "fouls_committed": ["exact", "gte", "lte", "range"],
        "fouls_won": ["exact", "gte", "lte", "range"],
        "player__full_name": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
        "league__code": ["exact"],
        "league__name": ["exact"],
        "season__season": ["exact"],
        "position": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "matches_completed": ["exact", "gte", "lte", "range"],
        "matches_substituted": ["exact", "gte", "lte", "range"],
        "unused_sub": ["exact", "gte", "lte", "range"],
        "goals": ["exact", "gte", "lte", "range"],
        "assists": ["exact", "gte", "lte", "range"],
        "xg": ["exact", "gte", "lte", "range"],
        "npxg": ["exact", "gte", "lte", "range"],
        "xg_performance": ["exact", "gte", "lte", "range"],
        "npxg_performance": ["exact", "gte", "lte", "range"],
        "prog_carrides": ["exact", "gte", "lte", "range"],
        "prog_carries_final_3rd": ["exact", "gte", "lte", "range"],
        "prog_passes": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes_to_final_3rd": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
        "pass_switches": ["exact", "gte", "lte", "range"],
        "through_ball": ["exact", "gte", "lte", "range"],
        "shots_creation_action": ["exact", "gte", "lte", "range"],
        "offsides": ["exact", "gte", "lte", "range"],
        "pen_won": ["exact", "gte", "lte", "range"],
        "pen_conceded": ["exact", "gte", "lte", "range"],
        "tackles": ["exact", "gte", "lte", "range"],
        "tackles_won": ["exact", "gte", "lte", "range"],
        "interceptions": ["exact", "gte", "lte", "range"],
        "ball_recoveries": ["exact", "gte", "lte", "range"],
        "aerial_duels_won": ["exact", "gte", "lte", "range"],
        "aerial_duels_lost": ["exact", "gte", "lte", "range"],
        "blocks": ["exact", "gte", "lte", "range"],
        "touches": ["exact", "gte", "lte", "range"],
        "dispossessed": ["exact", "gte", "lte", "range"],
        "miscontrols": ["exact", "gte", "lte", "range"],
        "take_ons": ["exact", "gte", "lte", "range"],
        "take_ons_won": ["exact", "gte", "lte", "range"],
        "carries_to_final_3rd": ["exact", "gte", "lte", "range"],
        "carries_to_pen_area": ["exact", "gte", "lte", "range"],
        "yellow_card": ["exact", "gte", "lte", "range"],
        "red_card": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = PlayerSeasonStats.objects.select_related(
            "player", "club", "season"
        ).filter(club_id=club_id)
        return queryset


class ClubGoalkeeperView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = GoalkeeperSerializer

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "player__full_name",
        "club__name",
        "season__season",
        "age",
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "shots_faced",
        "saves",
        "save_percentage",
        "clean_sheets",
        "psxg",
        "psxg_performance",
        "pen_saved",
        "passes",
        "crosses_stopped",
        "sweeper_action",
        "sweeper_action_per90",
    ]
    search_fields = [
        "player__full_name",
        "club__name",
        "season__season",
        "age",
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "shots_faced",
        "saves",
        "save_percentage",
        "clean_sheets",
        "psxg",
        "psxg_performance",
        "pen_saved",
        "passes",
        "crosses_stopped",
        "sweeper_action",
        "sweeper_action_per90",
    ]
    ordering = [
        "matches_played",
        "minutes_played",
        "goals_conceded",
        "psxg",
        "player__full_name",
    ]
    filterset_fields = {
        "player__full_name": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
        "season__season": ["exact"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "shots_faced": ["exact", "gte", "lte", "range"],
        "saves": ["exact", "gte", "lte", "range"],
        "save_percentage": ["exact", "gte", "lte", "range"],
        "clean_sheets": ["exact", "gte", "lte", "range"],
        "psxg": ["exact", "gte", "lte", "range"],
        "psxg_performance": ["exact", "gte", "lte", "range"],
        "pen_saved": ["exact", "gte", "lte", "range"],
        "passes": ["exact", "gte", "lte", "range"],
        "crosses_stopped": ["exact", "gte", "lte", "range"],
        "sweeper_action": ["exact", "gte", "lte", "range"],
        "sweeper_action_per90": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = Goalkeeper.objects.select_related("player", "club", "season").filter(
            club_id=club_id
        )
        return queryset
