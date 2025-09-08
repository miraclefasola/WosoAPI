from rest_framework import serializers
from api.models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "code"]


class LeagueSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), source="country", write_only=True
    )
    country = serializers.ReadOnlyField(source="country.name")

    class Meta:
        model = League
        fields = ["id", "name", "country", "country_id", "code", "total_clubs"]


class SeasonSerializer(serializers.ModelSerializer):
    league_id = serializers.PrimaryKeyRelatedField(
        queryset=League.objects.all(), source="league", write_only=True
    )
    league = serializers.ReadOnlyField(source="league.name")

    class Meta:
        model = Season
        fields = ["id", "season", "league", "league_id"]


class ClubSerializer(serializers.ModelSerializer):


    class Meta:
        model = Club
        fields = ["id", "name", "fbref_id","stadium" ]


class ClubSeasonStatSerializer(serializers.ModelSerializer):
    club_id = serializers.PrimaryKeyRelatedField(
        queryset=Club.objects.all(), source="club", write_only=True
    )
    season_id = serializers.PrimaryKeyRelatedField(
        queryset=Season.objects.all(), source="season", write_only=True
    )
    league_id = serializers.PrimaryKeyRelatedField(
        queryset=League.objects.all(), source="league", write_only=True
    )
    league = serializers.ReadOnlyField(source="league.name")
    club = serializers.ReadOnlyField(source="club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = ClubSeasonStat
        fields = [
            "id",
            "club",
            "season",
            "club_id",
            "season_id",
            "league", 
            "league_id",
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


class PlayerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Player
        fields = ["id", "full_name", "fbref_id", "nationality","age"]


class PlayerSeasonStatsSerializer(serializers.ModelSerializer):
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source="player", write_only=True
    )
    season_id = serializers.PrimaryKeyRelatedField(
        queryset=Season.objects.all(), source="season", write_only=True
    )
    
    club_id= serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), source='club', write_only=True)
    player_name = serializers.ReadOnlyField(source="player.full_name")
    club_name = serializers.ReadOnlyField(source="club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = PlayerSeasonStats
        fields = [
            "id",
            "player_name",
            "club_name",
            "season",
            "player_id",
            "season_id",
            "club_id",
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
            "fouls_won",
            "fouls_commited",
            "carries_to_final_3rd",
            "carries_to_pen_area",
            "yellow_card",
            "red_card",
        ]


class GoalkeeperSerializer(serializers.ModelSerializer):
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source="player", write_only=True
    )
    season_id = serializers.PrimaryKeyRelatedField(
        queryset=Season.objects.all(), source="season", write_only=True
    )
    club_id= serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), source='club', write_only=True)
    player_name = serializers.ReadOnlyField(source="player.full_name")
    club_name = serializers.ReadOnlyField(source="club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = Goalkeeper
        fields = [
            "player_name",
            "club_name",
            "season",
            "player_id",
            "season_id",
            "club_id",
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
