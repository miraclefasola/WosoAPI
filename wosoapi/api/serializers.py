from rest_framework import serializers
from api.models import *


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class LeagueSerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source="country.name")

    class Meta:
        model = League
        fields = ["id", "name", "country"]


class SeasonSerializer(serializers.ModelSerializer):
    league = serializers.ReadOnlyField(source="league.name")

    class Meta:
        model = Season
        fields = ["id", "season", "league"]


class ClubSerializer(serializers.ModelSerializer):
    league = serializers.ReadOnlyField(source="league.name")

    class Meta:
        model = Club
        fields = ["id", "name", "fbref_id", "league"]


class ClubSeasonStatSerializer(serializers.ModelSerializer):
    club = serializers.ReadOnlyField(source="club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = ClubSeasonStat
        fields = [
            "id",
            "club",
            "season",
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
    club = serializers.ReadOnlyField(source="club.name")

    class Meta:
        model = Player
        fields = ["id", "full_name", "fbref_id", "club"]


class PlayerSeasonStatsSerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source="player.full_name")
    club_name = serializers.ReadOnlyField(source="player.club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = PlayerSeasonStats
        fields = [
            "id",
            "player_name",
            "club_name",
            "season",
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


class GoalkeeperSerializer(serializers.ModelSerializer):
    player_name = serializers.ReadOnlyField(source="player.full_name")
    club_name = serializers.ReadOnlyField(source="player.club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = Goalkeeper
        fields = [
            "player_name",
            "club_name",
            "season",
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
