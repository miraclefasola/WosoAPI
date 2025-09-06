import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
import numpy as np
from api.models import Player, Season, Goalkeeper


def get_numeric_value(value):
    """Converts a value to None if it is NaN, otherwise returns the value."""
    return None if pd.isna(value) else value


class Command(BaseCommand):
    help = "Imports goalkeeper season stats from a combined CSV, updating existing records."

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file", type=str, help="The path to the combined CSV file."
        )
        parser.add_argument(
            "--season_id",
            type=int,
            required=True,
            help="The ID of the season to associate the stats with.",
        )

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csv_file"]
        season_id = kwargs["season_id"]

        try:
            season = Season.objects.get(pk=season_id)
        except Season.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Season with ID {season_id} does not exist.")
            )
            return

        try:
            self.stdout.write(f"Reading data from {csv_file_path}...")
            df = pd.read_csv(csv_file_path)

            goalkeepers_df = df[df["position"] == "GK"]
            self.stdout.write(
                f"Importing stats for {len(goalkeepers_df)} goalkeepers..."
            )

            for index, row in goalkeepers_df.iterrows():
                try:
                    player, created_player = Player.objects.get_or_create(
                        fbref_id=row["player_id"], defaults={"name": row["player_name"]}
                    )

                    defaults = {
                        "position": get_numeric_value(row.get("position")),
                        "age": get_numeric_value(row.get("age")),
                        "matches_played": get_numeric_value(row.get("gk_games")),
                        "minutes_played": get_numeric_value(row.get("gk_minutes")),
                        "goals_conceded": get_numeric_value(
                            row.get("gk_goals_against")
                        ),
                        "shots_faced": get_numeric_value(
                            row.get("gk_shots_on_target_against")
                        ),
                        "saves": get_numeric_value(row.get("gk_saves")),
                        "save_percentage": get_numeric_value(row.get("gk_save_pct")),
                        "clean_sheets": get_numeric_value(row.get("gk_clean_sheets")),
                        "psxg": get_numeric_value(row.get("gk_psxg")),
                    }

                    obj, created = Goalkeeper.objects.update_or_create(
                        player=player, season=season, defaults=defaults
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created new stats for goalkeeper: {row["player_name"]}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Updated existing stats for goalkeeper: {row["player_name"]}'
                            )
                        )

                except KeyError as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Missing a required column for goalkeeper {row["player_id"]}: {e}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error processing row for goalkeeper {row["player_id"]}: {e}'
                        )
                    )

            self.stdout.write(self.style.SUCCESS("Goalkeeper stats import completed."))
            self.stdout.write(
                self.style.SUCCESS("Full import process finished successfully.")
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'The file "{csv_file_path}" was not found.')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))


# python manage.py import_goalkeeper_stats WSL_2024_25_COMBINED_PLAYER_STATS.csv --season_id=3
