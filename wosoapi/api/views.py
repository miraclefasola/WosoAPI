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
    
    ordering_fields = ["id", "name"]
    search_fields = ["id", "name"]
    ordering=["name"]
    filterset_fields = ["id", "name"]


class LeagueView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    serializer_class = LeagueSerializer
    queryset = League.objects.all()
    authentication_classes = [JWTAuthentication]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    ordering_fields = ["id", "name", "country"]
    search_fields = ["id", "name", "country"]
    ordering=['name']
    filterset_fields = ["id", "name", "country"]

class SeasonView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    ordering_fields = ["id", "season", "league"]
    search_fields = ["id", "season", "league"]
    ordering=["season"]
    filterset_fields = ["id", "season", "league"]


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
    
    ordering_fields = ["id", "name", "fbref_id", "league"]
    search_fields = ["id", "name", "fbref_id", "league"]
    ordering=["name"]
    filterset_fields = ["id", "name", "fbref_id", "league"]


class ClubSeasonStatView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = ClubSeasonStat.objects.all()
    serializer_class = ClubSeasonStatSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    ordering_fields = ["id","club","season","points_won","league_position","matches_played","win","draw","lost","goals_scored","goals_conceded","xg_created","xg_conceded","shots","shots_target","passes","passes_comp","passes_to_final_third","passes_to_pen_area"]
    search_fields = ["id","club","season","points_won","league_position","matches_played","win","draw","lost","goals_scored","goals_conceded","xg_created","xg_conceded","shots","shots_target","passes","passes_comp","passes_to_final_third","passes_to_pen_area"]
    ordering=["league_position"]
    filterset_fields = ["id","club","season","points_won","league_position","matches_played","win","draw","lost","goals_scored","goals_conceded","xg_created","xg_conceded","shots","shots_target","passes","passes_comp","passes_to_final_third","passes_to_pen_area"]



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
    
    ordering_fields = ["id", "full_name", "fbref_id", "club"]
    search_fields = ["id", "full_name", "fbref_id", "club"]
    ordering=["full_name"]
    filterset_fields = ["id", "full_name", "fbref_id", "club"]
    


class PlayerSeasonStatsView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = PlayerSeasonStats.objects.all()
    serializer_class = PlayerSeasonStatsSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    ordering_fields = ["id", "player__full_name", "player__club__name", "season__season", "position", "age", "matches_played", "minutes_played", "goals", "assists", "xg", "npxg", "prog_carries", "shots_target", "passes_to_final_3rd", "passes_to_pen_area", "shots_creation_action", "tackles", "tackles_won", "interceptions", "touches", "take_ons", "carries_to_final_3rd", "carries_to_pen_area", "yellow_card", "red_card"
]
    search_fields = ["id", "player__full_name", "player__club__name", "season__season", "position", "age", "matches_played", "minutes_played", "goals", "assists", "xg", "npxg", "prog_carries", "shots_target", "passes_to_final_3rd", "passes_to_pen_area", "shots_creation_action", "tackles", "tackles_won", "interceptions", "touches", "take_ons", "carries_to_final_3rd", "carries_to_pen_area", "yellow_card", "red_card"]
    ordering=["position"]
    filterset_fields = ["id", "player__full_name", "player__club__name", "season__season", "position", "age", "matches_played", "minutes_played", "goals", "assists", "xg", "npxg", "prog_carries", "shots_target", "passes_to_final_3rd", "passes_to_pen_area", "shots_creation_action", "tackles", "tackles_won", "interceptions", "touches", "take_ons", "carries_to_final_3rd", "carries_to_pen_area", "yellow_card", "red_card"
]


class GoalkeeperView(ModelViewSet):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = Goalkeeper.objects.all()
    serializer_class = GoalkeeperSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    ordering_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"
]
    search_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"
]
    ordering=["matches_played"]
    filterset_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"
]


class LeagueSeasonView(ListAPIView):
    permission_classes = [IsSuperUserOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = SeasonSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    ordering_fields = ["id", "season", "league"]
    search_fields = ["id", "season", "league"]
    ordering=["season"]
    filterset_fields = ["id", "season", "league"]


    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Season.objects.filter(league_id=league_id)
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
    
    ordering_fields = ["id", "name", "fbref_id", "league"]
    search_fields = ["id", "name", "fbref_id", "league"]
    ordering=["league_position"]
    filterset_fields = ["id", "name", "fbref_id", "league"]

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Club.objects.filter(league_id=league_id)
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
    
    ordering_fields = ["id", "full_name", "fbref_id", "club"]
    search_fields = ["id", "full_name", "fbref_id", "club"]
    ordering=["full_name"]
    filterset_fields = ["id", "full_name", "fbref_id", "club"]
    

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Player.objects.filter(club__league_id=league_id)
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
    
    ordering_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"]
    search_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"]
    ordering=["matches_played"]
    filterset_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"]

    def get_queryset(self):
        league_id = self.kwargs.get("league_id")
        get_object_or_404(League, pk=league_id)
        queryset = Goalkeeper.objects.filter(club__league_id=league_id)
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
    
    ordering_fields = ["id","club","season","points_won","league_position","matches_played","win","draw","lost","goals_scored","goals_conceded","xg_created","xg_conceded","shots","shots_target","passes","passes_comp","passes_to_final_third","passes_to_pen_area"]
    search_fields = ["id","club","season","points_won","league_position","matches_played","win","draw","lost","goals_scored","goals_conceded","xg_created","xg_conceded","shots","shots_target","passes","passes_comp","passes_to_final_third","passes_to_pen_area"]
    ordering=["league_position"]
    filterset_fields = ["id","club","season","points_won","league_position","matches_played","win","draw","lost","goals_scored","goals_conceded","xg_created","xg_conceded","shots","shots_target","passes","passes_comp","passes_to_final_third","passes_to_pen_area"]

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = ClubSeasonStat.objects.filter(club_id=club_id)
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
    ordering_fields = ["id", "player__full_name", "player__club__name", "season__season", "position", "age", "matches_played", "minutes_played", "goals", "assists", "xg", "npxg", "prog_carries", "shots_target", "passes_to_final_3rd", "passes_to_pen_area", "shots_creation_action", "tackles", "tackles_won", "interceptions", "touches", "take_ons", "carries_to_final_3rd", "carries_to_pen_area", "yellow_card", "red_card"
]
    search_fields = ["id", "player__full_name", "player__club__name", "season__season", "position", "age", "matches_played", "minutes_played", "goals", "assists", "xg", "npxg", "prog_carries", "shots_target", "passes_to_final_3rd", "passes_to_pen_area", "shots_creation_action", "tackles", "tackles_won", "interceptions", "touches", "take_ons", "carries_to_final_3rd", "carries_to_pen_area", "yellow_card", "red_card"]
    ordering=["position"]
    filterset_fields = ["id", "player__full_name", "player__club__name", "season__season", "position", "age", "matches_played", "minutes_played", "goals", "assists", "xg", "npxg", "prog_carries", "shots_target", "passes_to_final_3rd", "passes_to_pen_area", "shots_creation_action", "tackles", "tackles_won", "interceptions", "touches", "take_ons", "carries_to_final_3rd", "carries_to_pen_area", "yellow_card", "red_card"
]

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = PlayerSeasonStats.objects.filter(player__club_id=club_id)
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
    
    ordering_fields = ["id","player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"]
    search_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"]
    ordering=["matches_played"]
    filterset_fields = ["player__full_name", "player__club__name", "season__season", "age", "matches_played", "minutes_played", "goals_conceded", "shots_faced", "saves", "save_percentage", "clean_sheets", "psxg"]

    def get_queryset(self):
        club_id = self.kwargs.get("club_id")
        get_object_or_404(Club, pk=club_id)
        queryset = Goalkeeper.objects.filter(player__club_id=club_id)
        return queryset
