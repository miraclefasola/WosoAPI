from django.http import Http404
from django.shortcuts import render

from api.models import *
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from itertools import groupby
from django.db.models import F, Q, Value
from django.db.models.functions import Replace
from django.http import HttpResponse


class HomeView(ListView):
    queryset = League.objects.all()
    template_name = "core/home.html"
    context_object_name = "leagues"


class LeagueSeasonDetailView(DetailView):
    model = ClubSeasonStat
    template_name = "core/clubs.html"
    context_object_name = "league"

    def get_object(self):
        league_code = self.kwargs.get("league_code")
        return get_object_or_404(League, code=league_code)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = self.get_object()

        base_qs = ClubSeasonStat.objects.select_related(
            "club", "season", "league"
        ).filter(league=league)
        distinct_qs = PlayerSeasonStats.objects.select_related(
            "club", "season", "player"
        ).filter(league=league)

        goalkeeper_qs = Goalkeeper.objects.select_related(
            "player", "club", "season"
        ).filter(league=league)

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
            field_name = orderby.lstrip("-")
            for season in seasons:
                season_players = qs.filter(season__season=season)
                field_kwargs = {f"{field_name}__gt": 0}
                top10 = season_players.filter(**field_kwargs).order_by(orderby)[:10]

                grouped[season] = list(top10)
            return grouped

        goal_diff = base_qs.annotate(goal_diff=F("goals_scored") - F("goals_conceded"))
        distinct_qs = distinct_qs.annotate(GA=F("goals") + F("assists"))

        def U23_stats(qs, orderby):
            seasons = qs.values_list("season__season", flat=True).distinct()
            grouped = {}

            field_name = orderby.lstrip("-")

            for season in seasons:

                season_qs = qs.filter(season__season=season).exclude(player__age__gt=23)

                filter_kwargs = {f"{field_name}__gt": 0}
                season_qs = season_qs.filter(**filter_kwargs)

                top10 = season_qs.order_by(orderby)[:10]
                grouped[season] = list(top10)

            return grouped

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
        context["player_GA"] = group_by_distinct(distinct_qs, "-GA")
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
        context["U23_player_minutes"] = U23_stats(distinct_qs, "-minutes_played")
        context["U23_player_games_completed"] = U23_stats(
            distinct_qs, "-matches_completed"
        )
        context["U23_player_matches_played"] = U23_stats(distinct_qs, "-matches_played")
        context["U23_player_minutes_played"] = U23_stats(distinct_qs, "-minutes_played")
        context["U23_player_matches_substituted"] = U23_stats(
            distinct_qs, "-matches_substituted"
        )
        context["U23_player_unused_sub"] = U23_stats(distinct_qs, "-unused_sub")
        context["U23_player_goals"] = U23_stats(distinct_qs, "-goals")
        context["U23_player_assists"] = U23_stats(distinct_qs, "-assists")
        context["U23_player_GA"] = U23_stats(distinct_qs, "-GA")
        context["U23_player_xg"] = U23_stats(distinct_qs, "-xg")
        context["U23_player_npxg"] = U23_stats(distinct_qs, "-npxg")
        context["U23_player_xg_performance"] = U23_stats(distinct_qs, "-xg_performance")
        context["U23_player_npxg_performance"] = U23_stats(
            distinct_qs, "-npxg_performance"
        )
        context["U23_player_prog_carries"] = U23_stats(distinct_qs, "-prog_carries")
        context["U23_player_prog_carries_final_3rd"] = U23_stats(
            distinct_qs, "-prog_carries_final_3rd"
        )
        context["U23_player_prog_passes"] = U23_stats(distinct_qs, "-prog_passes")
        context["U23_player_shots_target"] = U23_stats(distinct_qs, "-shots_target")
        context["U23_player_passes_to_final_3rd"] = U23_stats(
            distinct_qs, "-passes_to_final_3rd"
        )
        context["U23_player_passes_to_pen_area"] = U23_stats(
            distinct_qs, "-passes_to_pen_area"
        )
        context["U23_player_pass_switches"] = U23_stats(distinct_qs, "-pass_switches")
        context["U23_player_through_ball"] = U23_stats(distinct_qs, "-through_ball")
        context["U23_player_shots_creation_action"] = U23_stats(
            distinct_qs, "-shots_creation_action"
        )
        context["U23_player_offsides"] = U23_stats(distinct_qs, "-offsides")
        context["U23_player_pen_won"] = U23_stats(distinct_qs, "-pen_won")
        context["U23_player_pen_conceded"] = U23_stats(distinct_qs, "-pen_conceded")
        context["U23_player_tackles"] = U23_stats(distinct_qs, "-tackles")
        context["U23_player_ball_recoveries"] = U23_stats(
            distinct_qs, "-ball_recoveries"
        )
        context["U23_player_aerial_duels_won"] = U23_stats(
            distinct_qs, "-aerial_duels_won"
        )
        context["U23_player_aerial_duels_lost"] = U23_stats(
            distinct_qs, "-aerial_duels_lost"
        )
        context["U23_player_blocks"] = U23_stats(distinct_qs, "-blocks")
        context["U23_player_tackles_won"] = U23_stats(distinct_qs, "-tackles_won")
        context["U23_player_interceptions"] = U23_stats(distinct_qs, "-interceptions")
        context["U23_player_touches"] = U23_stats(distinct_qs, "-touches")
        context["U23_player_dispossessed"] = U23_stats(distinct_qs, "-dispossessed")
        context["U23_player_miscontrols"] = U23_stats(distinct_qs, "-miscontrols")
        context["U23_player_take_ons"] = U23_stats(distinct_qs, "-take_ons")
        context["U23_player_take_ons_won"] = U23_stats(distinct_qs, "-take_ons_won")
        context["U23_player_fouls_won"] = U23_stats(distinct_qs, "-fouls_won")
        context["U23_player_fouls_committed"] = U23_stats(
            distinct_qs, "-fouls_committed"
        )
        context["U23_player_carries_to_final_3rd"] = U23_stats(
            distinct_qs, "-carries_to_final_3rd"
        )
        context["U23_player_carries_to_pen_area"] = U23_stats(
            distinct_qs, "-carries_to_pen_area"
        )
        context["U23_player_yellow_card"] = U23_stats(distinct_qs, "-yellow_card")
        context["U23_player_red_card"] = U23_stats(distinct_qs, "-red_card")
        context["goalkeeper_games_played"] = group_by_distinct(
            goalkeeper_qs, "-matches_played"
        )
        context["goalkeeper_minutes_played"] = group_by_distinct(
            goalkeeper_qs, "minutes_played"
        )
        context["goalkeeper_goals_conceded"] = group_by_distinct(
            goalkeeper_qs, "-goals_conceded"
        )
        context["goalkeeper_shots_faced"] = group_by_distinct(
            goalkeeper_qs, "-shots_faced"
        )
        context["goalkeeper_saves"] = group_by_distinct(goalkeeper_qs, "-saves")
        context["goalkeeper_save_percentage"] = group_by_distinct(
            goalkeeper_qs, "-save_percentage"
        )
        context["goalkeeper_clean_sheets"] = group_by_distinct(
            goalkeeper_qs, "-clean_sheets"
        )
        context["goalkeeper_psxg"] = group_by_distinct(goalkeeper_qs, "-psxg")
        context["goalkeeper_psxg_performance"] = group_by_distinct(
            goalkeeper_qs, "-psxg_performance"
        )
        context["goalkeeper_pen_saved"] = group_by_distinct(goalkeeper_qs, "-pen_saved")
        context["goalkeeper_passes"] = group_by_distinct(goalkeeper_qs, "-passes")
        context["goalkeeper_crosses_stopped"] = group_by_distinct(
            goalkeeper_qs, "-crosses_stopped"
        )
        context["goalkeeper_sweeper_action"] = group_by_distinct(
            goalkeeper_qs, "-sweeper_action"
        )
        context["goalkeeper_sweeper_action_per90"] = group_by_distinct(
            goalkeeper_qs, "-sweeper_action_per90"
        )

        return context


class ClubSeasonStatView(DetailView):
    model = ClubSeasonStat
    template_name = "core/clubstats.html"
    context_object_name = "club"

    def get_object(self):
        club = self.kwargs.get("club_name")
        club_param = club.replace(" ", "").replace("-", "")

        try:
            club_id = int(club)
            search = (
                ClubSeasonStat.objects.filter(club__id=club_id)
                .order_by("-season__season")
                .first()
            )
            return search

        except ClubSeasonStat.MultipleObjectsReturned:
            search = (
                ClubSeasonStat.objects.filter(club__name__iexact=club)
                .order_by("-season__season")
                .first()
            )
            return search
        except ValueError:
            normalized = club.replace(" ", "").replace("-", "")
            search = (
                ClubSeasonStat.objects.annotate(
                    normalized_name=Replace(
                        Replace(F("club__name"), Value(" "), Value("")),
                        Value("-"),
                        Value(""),
                    )
                )
                .filter(
                    Q(normalized_name__icontains=normalized)
                    | Q(club__fbref_id__iexact=club)
                )
                .order_by("-season__season")
                .first()
            )

        if search is None:
            raise Http404(f"Club '{club}' not found")
        print(search)
        return search

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.get_object()
        player_qs = PlayerSeasonStats.objects.select_related(
            "club", "season", "player"
        ).filter(club=club.club)
        goalkeeper_qs = Goalkeeper.objects.select_related(
            "player", "club", "season"
        ).filter(club=club.club)
        player_qs = player_qs.annotate(GA=F("goals") + F("assists"))
        all_seasons = ClubSeasonStat.objects.filter(club=club.club).order_by(
            "-season__season"
        )

        def get_season(obj):
            return obj.season.season

        def group_by_season(qs, orderby):
            ordered = qs.order_by("season__season", orderby)
            grouped = {}

            for season, obj in groupby(ordered, get_season):
                grouped[season] = list(obj)
            return grouped

        def Top_players(qs, orderby):
            seasons = qs.values_list("season__season", flat=True).distinct()
            grouped = {}
            field_name = orderby.lstrip("-")
            for season in seasons:
                zero_filter = {f"{field_name}__gt": 0}
                season_query = qs.filter(season__season=season)
                top10 = season_query.filter(**zero_filter).order_by(orderby)[:10]
                grouped[season] = list(top10)
            return grouped

        context["player_games_completed"] = Top_players(player_qs, "-matches_completed")
        context["player_matches_played"] = Top_players(player_qs, "-matches_played")
        context["player_minutes_played"] = Top_players(player_qs, "-minutes_played")
        context["player_matches_substituted"] = Top_players(
            player_qs, "-matches_substituted"
        )
        context["player_unused_sub"] = Top_players(player_qs, "-unused_sub")
        context["player_goals"] = Top_players(player_qs, "-goals")
        context["player_assists"] = Top_players(player_qs, "-assists")
        context["player_GA"] = Top_players(player_qs, "-GA")
        context["player_xg"] = Top_players(player_qs, "-xg")
        context["player_npxg"] = Top_players(player_qs, "-npxg")
        context["player_xg_performance"] = Top_players(player_qs, "-xg_performance")
        context["player_npxg_performance"] = Top_players(player_qs, "-npxg_performance")
        context["player_prog_carries"] = Top_players(player_qs, "-prog_carries")
        context["player_prog_carries_final_3rd"] = Top_players(
            player_qs, "-prog_carries_final_3rd"
        )
        context["player_prog_passes"] = Top_players(player_qs, "-prog_passes")
        context["player_shots_target"] = Top_players(player_qs, "-shots_target")
        context["player_passes_to_final_3rd"] = Top_players(
            player_qs, "-passes_to_final_3rd"
        )
        context["player_passes_to_pen_area"] = Top_players(
            player_qs, "-passes_to_pen_area"
        )
        context["player_pass_switches"] = Top_players(player_qs, "-pass_switches")
        context["player_through_ball"] = Top_players(player_qs, "-through_ball")
        context["player_shots_creation_action"] = Top_players(
            player_qs, "-shots_creation_action"
        )
        context["player_offsides"] = Top_players(player_qs, "-offsides")
        context["player_pen_won"] = Top_players(player_qs, "-pen_won")
        context["player_pen_conceded"] = Top_players(player_qs, "-pen_conceded")
        context["player_tackles"] = Top_players(player_qs, "-tackles")
        context["player_ball_recoveries"] = Top_players(player_qs, "-ball_recoveries")
        context["player_aerial_duels_won"] = Top_players(player_qs, "-aerial_duels_won")
        context["player_aerial_duels_lost"] = Top_players(
            player_qs, "-aerial_duels_lost"
        )
        context["player_blocks"] = Top_players(player_qs, "-blocks")
        context["player_tackles_won"] = Top_players(player_qs, "-tackles_won")
        context["player_interceptions"] = Top_players(player_qs, "-interceptions")
        context["player_touches"] = Top_players(player_qs, "-touches")
        context["player_dispossessed"] = Top_players(player_qs, "-dispossessed")
        context["player_miscontrols"] = Top_players(player_qs, "-miscontrols")
        context["player_take_ons"] = Top_players(player_qs, "-take_ons")
        context["player_take_ons_won"] = Top_players(player_qs, "-take_ons_won")
        context["player_fouls_won"] = Top_players(player_qs, "-fouls_won")
        context["player_fouls_committed"] = Top_players(player_qs, "-fouls_committed")
        context["player_carries_to_final_3rd"] = Top_players(
            player_qs, "-carries_to_final_3rd"
        )
        context["player_carries_to_pen_area"] = Top_players(
            player_qs, "-carries_to_pen_area"
        )
        context["player_yellow_card"] = Top_players(player_qs, "-yellow_card")
        context["player_red_card"] = Top_players(player_qs, "-red_card")
        context["goalkeeper_games_played"] = Top_players(
            goalkeeper_qs, "-matches_played"
        )
        context["goalkeeper_minutes_played"] = Top_players(
            goalkeeper_qs, "minutes_played"
        )
        context["goalkeeper_goals_conceded"] = Top_players(
            goalkeeper_qs, "-goals_conceded"
        )
        context["goalkeeper_shots_faced"] = Top_players(goalkeeper_qs, "-shots_faced")
        context["goalkeeper_saves"] = Top_players(goalkeeper_qs, "-saves")
        context["goalkeeper_save_percentage"] = Top_players(
            goalkeeper_qs, "-save_percentage"
        )
        context["goalkeeper_clean_sheets"] = Top_players(goalkeeper_qs, "-clean_sheets")
        context["goalkeeper_psxg"] = Top_players(goalkeeper_qs, "-psxg")
        context["goalkeeper_psxg_performance"] = Top_players(
            goalkeeper_qs, "-psxg_performance"
        )
        context["goalkeeper_pen_saved"] = Top_players(goalkeeper_qs, "-pen_saved")
        context["goalkeeper_passes"] = Top_players(goalkeeper_qs, "-passes")
        context["goalkeeper_crosses_stopped"] = Top_players(
            goalkeeper_qs, "-crosses_stopped"
        )
        context["goalkeeper_sweeper_action"] = Top_players(
            goalkeeper_qs, "-sweeper_action"
        )
        context["goalkeeper_sweeper_action_per90"] = Top_players(
            goalkeeper_qs, "-sweeper_action_per90"
        )

        context["player_season"] = group_by_season(player_qs, "-position")
        context["all_seasons"] = all_seasons
        context["goalkeeper_season"] = group_by_season(
            goalkeeper_qs, "player__full_name"
        )

        return context


class PlayerSeasonDetailView(DetailView):
    model = PlayerSeasonStats
    template_name = "core/player.html"
    context_object_name = "player"

    def get_object(self):
        player = self.kwargs.get("player_id")
        normalized_name = player.replace(" ", "").replace("-", "")

        # First: Try PlayerSeasonStats
        try:
            search = PlayerSeasonStats.objects.get(
                Q(player__full_name__iexact=player) | Q(player__fbref_id=player)
            )

            return search
        except PlayerSeasonStats.DoesNotExist:
            pass
        except PlayerSeasonStats.MultipleObjectsReturned:
            search = (
                PlayerSeasonStats.objects.annotate(
                    normalized=Replace(
                        Replace(F("player__full_name"), Value(" "), Value("")),
                        Value("-"),
                        Value(""),
                    )
                )
                .filter(normalized__icontains=normalized_name)
                .order_by("season__season")
                .first()
            )
            if search:

                return search

        # Second: Try Goalkeeper model
        try:
            return Goalkeeper.objects.get(
                Q(player__full_name__iexact=player) | Q(player__fbref_id=player)
            )
        except Goalkeeper.DoesNotExist:
            pass
        except Goalkeeper.MultipleObjectsReturned:
            search = (
                Goalkeeper.objects.annotate(
                    normalized=Replace(
                        Replace(F("player__full_name"), Value(" "), Value("")),
                        Value("-"),
                        Value(""),
                    )
                )
                .filter(normalized__icontains=normalized_name)
                .order_by("season__season")
                .first()
            )
            if search:
                return search

        try:
            player_id = int(player)
            return PlayerSeasonStats.objects.get(player__id=player_id)
        except (ValueError, PlayerSeasonStats.DoesNotExist):
            try:
                return Goalkeeper.objects.get(player__id=player_id)
            except Goalkeeper.DoesNotExist:
                raise Http404(f"Stats for {player} not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_player_season = self.object
        if isinstance(current_player_season, PlayerSeasonStats):
            player_qs = (
                PlayerSeasonStats.objects.select_related("club", "season", "player")
                .filter(player=current_player_season.player)
                .order_by("season__season")
            )
        else:
            player_qs = (
                Goalkeeper.objects.select_related("club", "season", "player")
                .filter(player=current_player_season.player)
                .order_by("season__season")
            )
        if current_player_season.player.nationality:
            nationality = current_player_season.player.nationality.strip()
            parts = nationality.split()

            if len(parts) > 1:
                cleaned_nationality = " ".join(parts[1:])
            else:
                cleaned_nationality = parts[0]
                return cleaned_nationality
        else:
            cleaned_nationality = "Unknown"

        context["player_profile"] = cleaned_nationality
        context["players"] = player_qs
        context["is_goalkeeper"] = isinstance(current_player_season, Goalkeeper)
        context["ga"] = getattr(current_player_season, "goals", 0) + getattr(
            current_player_season, "assists", 0
        )
        return context
