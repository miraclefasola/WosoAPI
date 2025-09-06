import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Club, Season, ClubSeasonStat


class Command(BaseCommand):
    help = "Imports a single club's season stats from a CSV for a given season."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The path to the CSV file.")
        parser.add_argument(
            "--season_id",
            type=int,
            required=True,
            help="The ID of the season to associate the stats with.",
        )
        parser.add_argument(
            "--club_fbref_id",
            type=str,
            required=True,
            help="The fbref_id of the club to import stats for.",
        )

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csv_file"]
        season_id = kwargs["season_id"]
        club_fbref_id = kwargs["club_fbref_id"]

        try:
            # Get the Season and Club objects
            season = Season.objects.get(pk=season_id)
            club = Club.objects.get(fbref_id=club_fbref_id)
        except (Season.DoesNotExist, Club.DoesNotExist) as e:
            self.stdout.write(self.style.ERROR(e))
            return

        try:
            # Read the CSV and find the specific row for the club
            df = pd.read_csv(csv_file_path)
            row = df[df["team_id"] == club_fbref_id].iloc[0]

            # Map CSV columns to model fields
            stats_to_import = {
                "points_won": row["points"],
                "league_position": row["rank"],
                "matches_played": row["games"],
                "win": row["wins"],
                "draw": row["ties"],
                "lost": row["losses"],
                "goals_scored": row["goals_for"],
                "goals_conceded": row["goals_against"],
                "xg_created": row["xg_for"],
                "xg_conceded": row["xg_against"],
                "shots": row["shots"],
                "shots_target": row["shots_on_target"],
                "passes": row["passes"],
                "passes_comp": row["passes_completed"],
                "passes_to_final_third": row["passes_into_final_third"],
                "passes_to_pen_area": row["passes_into_penalty_area"],
            }

            # Update or create the ClubSeasonStat record
            stat_obj, created = ClubSeasonStat.objects.update_or_create(
                club=club, season=season, defaults=stats_to_import
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created a new ClubSeasonStat for {club.name} in {season.season}."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully updated ClubSeasonStat for {club.name} in {season.season}."
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'The file "{csv_file_path}" was not found.')
            )
        except IndexError:
            self.stdout.write(
                self.style.ERROR(
                    f'Could not find a row with team_id "{club_fbref_id}" in the CSV.'
                )
            )
        except KeyError as e:
            self.stdout.write(
                self.style.ERROR(f"Missing a required column in the CSV file: {e}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))


# python manage.py import_club_stats WSL_2024_25_TEAM_STATS_20250821_102053.csv --season_id=3 --club_fbref_id=78ba1bd4
