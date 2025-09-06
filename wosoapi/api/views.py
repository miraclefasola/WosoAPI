from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from api.serializers import *
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.permissions import IsSuperUserOrReadOnly
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import filters, DjangoFilterBackend
from django_filters.filters import OrderingFilter
from rest_framework import filters


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
        "code": ["exact", "icontains"],
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
        "code": ["exact", "icontains"],
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
    ordering = ["season"]
    filterset_fields = {
        "id": ["exact"],
        "season": ["exact", "icontains"],
        "league__name": ["exact", "icontains"],
    }


class Clubview(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = ClubSerializer
    queryset = Club.objects.select_related("league").all()
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "name", "fbref_id", "league__name"]
    search_fields = ["id", "name", "fbref_id", "league__name"]
    ordering = ["name"]
    filterset_fields = {
        "id": ["exact"],
        "name": ["exact", "icontains"],
        "fbref_id": ["exact", "icontains"],
        "league__name": ["exact", "icontains"],
    }


class ClubSeasonStatView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = ClubSeasonStat.objects.select_related("club", "season").all()
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
        "shots",
        "shots_target",
        "passes",
        "passes_comp",
        "passes_to_final_third",
        "passes_to_pen_area",
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
        "shots",
        "shots_target",
        "passes",
        "passes_comp",
        "passes_to_final_third",
        "passes_to_pen_area",
    ]
    ordering = ["league_position"]
    filterset_fields = {
        "id": ["exact"],
        "club__name": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
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
        "shots": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes": ["exact", "gte", "lte", "range"],
        "passes_comp": ["exact", "gte", "lte", "range"],
        "passes_to_final_third": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
    }


class PlayerView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Player.objects.select_related("club").all()
    serializer_class = PlayerSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "full_name", "fbref_id", "club__name"]
    search_fields = ["id", "full_name", "fbref_id", "club__name"]
    ordering = ["full_name"]
    filterset_fields = {
        "id": ["exact"],
        "full_name": ["exact", "icontains"],
        "fbref_id": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
    }


class PlayerSeasonStatsView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = PlayerSeasonStats.objects.select_related("player", "player__club", "player__club__league", "season").all()
    serializer_class = PlayerSeasonStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = [
        "id",
        "fouls_commited",
        "fouls_won",
        "player__full_name",
        "player__club__name",
        "player__club__league__code",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "goals",
        "assists",
        "xg",
        "npxg",
        "prog_carries",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "shots_creation_action",
        "tackles",
        "tackles_won",
        "interceptions",
        "touches",
        "take_ons",
        "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    search_fields = [
        "id",
        "fouls_commited",
        "fouls_won",
        "player__full_name",
        "player__club__name",
        "player__club__league__code",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "goals",
        "assists",
        "xg",
        "npxg",
        "prog_carries",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "shots_creation_action",
        "tackles",
        "tackles_won",
        "interceptions",
        "touches",
        "take_ons",
        "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    ordering = ["position"]
    filterset_fields = {
        "id": ["exact"],
        "fouls_commited": ["exact", "gte", "lte", "range"],
        "fouls_won": ["exact", "gte", "lte", "range"],
        "player__full_name": ["exact", "icontains"],
        "player__club__name": ["exact", "icontains"],
        "player__club__league__code": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
        "position": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals": ["exact", "gte", "lte", "range"],
        "assists": ["exact", "gte", "lte", "range"],
        "xg": ["exact", "gte", "lte", "range"],
        "npxg": ["exact", "gte", "lte", "range"],
        "prog_carries": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes_to_final_3rd": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
        "shots_creation_action": ["exact", "gte", "lte", "range"],
        "tackles": ["exact", "gte", "lte", "range"],
        "tackles_won": ["exact", "gte", "lte", "range"],
        "interceptions": ["exact", "gte", "lte", "range"],
        "touches": ["exact", "gte", "lte", "range"],
        "take_ons": ["exact", "gte", "lte", "range"],
        "carries_to_final_3rd": ["exact", "gte", "lte", "range"],
        "carries_to_pen_area": ["exact", "gte", "lte", "range"],
        "yellow_card": ["exact", "gte", "lte", "range"],
        "red_card": ["exact", "gte", "lte", "range"],
    }


class GoalkeeperView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Goalkeeper.objects.select_related("player","player__club","player__club__league", "season").all()
    serializer_class = GoalkeeperSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]


    ordering_fields = [
        "player__full_name",
        "player__club__name",
        "player__club__league__code",
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
    ]
    search_fields = [
        "player__full_name",
        "player__club__name",
        "player__club__league__code",
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
    ]
    ordering = ["matches_played"]
    filterset_fields = {
        "player__full_name": ["exact", "icontains"],
        "player__club__name": ["exact", "icontains"],
        "player__club__league__code": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "shots_faced": ["exact", "gte", "lte", "range"],
        "saves": ["exact", "gte", "lte", "range"],
        "save_percentage": ["exact", "gte", "lte", "range"],
        "clean_sheets": ["exact", "gte", "lte", "range"],
        "psxg": ["exact", "gte", "lte", "range"],
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
    ordering = ["season"]
    filterset_fields = {
        "id": ["exact"],
        "season": ["exact", "icontains"],
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
    serializer_class = ClubSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "name", "fbref_id", "league__name"]
    search_fields = ["id", "name", "fbref_id", "league__name"]
    ordering = ["name"]
    filterset_fields = {
        "id": ["exact"],
        "name": ["exact", "icontains"],
        "fbref_id": ["exact", "icontains"],
        "league__name": ["exact", "icontains"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Club.objects.select_related("league").filter(league_id=league_id)
        return queryset


class LeaguePlayerView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlayerSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    ordering_fields = ["id", "full_name", "fbref_id", "club__name"]
    search_fields = ["id", "full_name", "fbref_id", "club__name"]
    ordering = ["full_name"]
    filterset_fields = {
        "id": ["exact"],
        "full_name": ["exact", "icontains"],
        "fbref_id": ["exact", "icontains"],
        "club__name": ["exact", "icontains"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Player.objects.select_related("club").filter(club__league_id=league_id)
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
        "player__club__name",
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
    ]
    search_fields = [
        "player__full_name",
        "player__club__name",
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
    ]
    ordering = ["matches_played"]
    filterset_fields = {
        "player__full_name": ["exact", "icontains"],
        "player__club__name": ["exact", "icontains"],
        "player__club__league__code": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "shots_faced": ["exact", "gte", "lte", "range"],
        "saves": ["exact", "gte", "lte", "range"],
        "save_percentage": ["exact", "gte", "lte", "range"],
        "clean_sheets": ["exact", "gte", "lte", "range"],
        "psxg": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Goalkeeper.objects.select_related("player","player__club", "player__club__league", "season").filter(player__club__league_id=league_id)
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
        "shots",
        "shots_target",
        "passes",
        "passes_comp",
        "passes_to_final_third",
        "passes_to_pen_area",
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
        "shots",
        "shots_target",
        "passes",
        "passes_comp",
        "passes_to_final_third",
        "passes_to_pen_area",
    ]
    ordering = ["league_position"]
    filterset_fields = {
        "id": ["exact"],
        "club__name": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
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
        "shots": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes": ["exact", "gte", "lte", "range"],
        "passes_comp": ["exact", "gte", "lte", "range"],
        "passes_to_final_third": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = ClubSeasonStat.objects.select_related("club", "season").filter(club_id=club_id)
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
        "fouls_commited",
        "fouls_won",
        "player__full_name",
        "player__club__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "goals",
        "assists",
        "xg",
        "npxg",
        "prog_carries",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "shots_creation_action",
        "tackles",
        "tackles_won",
        "interceptions",
        "touches",
        "take_ons",
        "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    search_fields = [
        "id",
        "fouls_commited",
        "fouls_won",
        "player__full_name",
        "player__club__name",
        "season__season",
        "position",
        "age",
        "matches_played",
        "minutes_played",
        "goals",
        "assists",
        "xg",
        "npxg",
        "prog_carries",
        "shots_target",
        "passes_to_final_3rd",
        "passes_to_pen_area",
        "shots_creation_action",
        "tackles",
        "tackles_won",
        "interceptions",
        "touches",
        "take_ons",
        "carries_to_final_3rd",
        "carries_to_pen_area",
        "yellow_card",
        "red_card",
    ]
    ordering = ["position"]
    filterset_fields = {
        "id": ["exact"],
        "fouls_commited": ["exact", "gte", "lte", "range"],
        "fouls_won": ["exact", "gte", "lte", "range"],
        "player__full_name": ["exact", "icontains"],
        "player__club__name": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
        "position": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals": ["exact", "gte", "lte", "range"],
        "assists": ["exact", "gte", "lte", "range"],
        "xg": ["exact", "gte", "lte", "range"],
        "npxg": ["exact", "gte", "lte", "range"],
        "prog_carries": ["exact", "gte", "lte", "range"],
        "shots_target": ["exact", "gte", "lte", "range"],
        "passes_to_final_3rd": ["exact", "gte", "lte", "range"],
        "passes_to_pen_area": ["exact", "gte", "lte", "range"],
        "shots_creation_action": ["exact", "gte", "lte", "range"],
        "tackles": ["exact", "gte", "lte", "range"],
        "tackles_won": ["exact", "gte", "lte", "range"],
        "interceptions": ["exact", "gte", "lte", "range"],
        "touches": ["exact", "gte", "lte", "range"],
        "take_ons": ["exact", "gte", "lte", "range"],
        "carries_to_final_3rd": ["exact", "gte", "lte", "range"],
        "carries_to_pen_area": ["exact", "gte", "lte", "range"],
        "yellow_card": ["exact", "gte", "lte", "range"],
        "red_card": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = PlayerSeasonStats.objects.select_related("player", "player__club", "season").filter(player__club_id=club_id)
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
        "player__club__name",
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
    ]
    search_fields = [
        "player__full_name",
        "player__club__name",
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
    ]
    ordering = ["matches_played"]
    filterset_fields = {
        "player__full_name": ["exact", "icontains"],
        "player__club__name": ["exact", "icontains"],
        "season__season": ["exact", "icontains"],
        "age": ["exact", "gte", "lte", "range"],
        "matches_played": ["exact", "gte", "lte", "range"],
        "minutes_played": ["exact", "gte", "lte", "range"],
        "goals_conceded": ["exact", "gte", "lte", "range"],
        "shots_faced": ["exact", "gte", "lte", "range"],
        "saves": ["exact", "gte", "lte", "range"],
        "save_percentage": ["exact", "gte", "lte", "range"],
        "clean_sheets": ["exact", "gte", "lte", "range"],
        "psxg": ["exact", "gte", "lte", "range"],
    }

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = Goalkeeper.objects.select_related("player", "player__club", "season").filter(player__club_id=club_id)
        return queryset