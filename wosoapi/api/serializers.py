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
        fields = ["id", "name", "fbref_id", "stadium"]


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
    league = serializers.ReadOnlyField(source="league.code")
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
            # Matches / Results
            "matches_played",
            "win",
            "draw",
            "lost",
            "points_won",
            "league_position",
            # Goals
            "goals_scored",
            "goals_conceded",
            # Expected goals
            "xg_created",
            "xg_conceded",
            # Shooting
            "shots",
            "shots_target",
            # Passing
            "passes",
            "passes_comp",
            "passes_to_final_third",
            "passes_to_pen_area",
        ]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "full_name", "fbref_id", "nationality", "age"]


class PlayerSeasonStatsSerializer(serializers.ModelSerializer):
    player_id = serializers.PrimaryKeyRelatedField(
        queryset=Player.objects.all(), source="player", write_only=True
    )
    season_id = serializers.PrimaryKeyRelatedField(
        queryset=Season.objects.all(), source="season", write_only=True
    )
    club_id = serializers.PrimaryKeyRelatedField(
        queryset=Club.objects.all(), source="club", write_only=True
    )
    league_id = serializers.PrimaryKeyRelatedField(
        queryset=League.objects.all(), source="league", write_only=True
    )
    league = serializers.ReadOnlyField(source="league.code")
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
            "league",
            "league_id",
            "player_id",
            "season_id",
            "club_id",
            "position",
            "age",
            # Matches
            "matches_played",
            "minutes_played",
            "matches_completed",
            "matches_substituted",
            "unused_sub",
            # Contributions
            "goals",
            "assists",
            # Expected goals
            "xg",
            "npxg",
            "xg_performance",
            "npxg_performance",
            # Carrying / Passing
            "prog_carries",
            "prog_carries_final_3rd",
            "carries_to_final_3rd",
            "carries_to_pen_area",
            "prog_passes",
            "passes_to_final_3rd",
            "passes_to_pen_area",
            "pass_switches",
            "through_ball",
            # Shooting / Creativity
            "shots_target",
            "shots_creation_action",
            "offsides",
            "pen_won",
            "pen_conceded",
            # Defensive actions
            "tackles",
            "tackles_won",
            "interceptions",
            "blocks",
            "ball_recoveries",
            "aerial_duels_won",
            "aerial_duels_lost",
            # Possession / touches
            "touches",
            "dispossessed",
            "miscontrols",
            "take_ons",
            # Discipline
            "fouls_won",
            "fouls_committed",
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
    club_id = serializers.PrimaryKeyRelatedField(
        queryset=Club.objects.all(), source="club", write_only=True
    )
    league_id = serializers.PrimaryKeyRelatedField(
        queryset=League.objects.all(), source="league", write_only=True
    )
    league = serializers.ReadOnlyField(source="league.code")
    player_name = serializers.ReadOnlyField(source="player.full_name")
    club_name = serializers.ReadOnlyField(source="club.name")
    season = serializers.ReadOnlyField(source="season.season")

    class Meta:
        model = Goalkeeper
        fields = [
            "player_name",
            "club_name",
            "season",
            "league",
            "league_id",
            "player_id",
            "season_id",
            "club_id",
            "position",
            "age",
            # Matches
            "matches_played",
            "minutes_played",
            # Goalkeeping
            "goals_conceded",
            "shots_faced",
            "saves",
            "save_percentage",
            "clean_sheets",
            # Advanced metrics
            "psxg",
            "psxg_performance",
            "pen_saved",
            # Distribution & command
            "passes",
            "crosses_stopped",
            # Sweeper actions
            "sweeper_action",
            "sweeper_action_per90",
        ]
