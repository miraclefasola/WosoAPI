import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
import numpy as np
from api.models import Player, Season, PlayerSeasonStats


def get_numeric_value(value):
    """Converts a value to None if it is NaN, otherwise returns the value."""
    return None if pd.isna(value) else value


class Command(BaseCommand):
    help = "Imports field player season stats from a combined CSV, updating existing records."

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

            field_players_df = df[df["position"] != "GK"]
            self.stdout.write(
                f"Importing stats for {len(field_players_df)} field players..."
            )

            for index, row in field_players_df.iterrows():
                try:
                    player, created_player = Player.objects.get_or_create(
                        fbref_id=row["player_id"], defaults={"name": row["player_name"]}
                    )

                    defaults = {
                        "position": get_numeric_value(row.get("position")),
                        "age": get_numeric_value(row.get("age")),
                        "matches_played": get_numeric_value(row.get("games")),
                        "minutes_played": get_numeric_value(row.get("minutes")),
                        "goals": get_numeric_value(row.get("goals")),
                        "assists": get_numeric_value(row.get("assists")),
                        "xg": get_numeric_value(row.get("xg")),
                        "npxg": get_numeric_value(row.get("npxg")),
                        "prog_carries": get_numeric_value(
                            row.get("progressive_carries")
                        ),
                        "shots_target": get_numeric_value(row.get("shots_on_target")),
                        "passes_to_final_3rd": get_numeric_value(
                            row.get("passes_into_final_third")
                        ),
                        "passes_to_pen_area": get_numeric_value(
                            row.get("passes_into_penalty_area")
                        ),
                        "shots_creation_action": get_numeric_value(row.get("sca")),
                        "tackles": get_numeric_value(row.get("tackles")),
                        "tackles_won": get_numeric_value(row.get("tackles_won")),
                        "interceptions": get_numeric_value(row.get("interceptions")),
                        "touches": get_numeric_value(row.get("touches")),
                        "take_ons": get_numeric_value(row.get("take_ons")),
                        "fouls_won": get_numeric_value(row.get("fouled")),
                        "fouls_commited": get_numeric_value(row.get("fouls")),
                        "carries_to_final_3rd": get_numeric_value(
                            row.get("carries_into_final_third")
                        ),
                        "carries_to_pen_area": get_numeric_value(
                            row.get("carries_into_penalty_area")
                        ),
                        "yellow_card": get_numeric_value(row.get("cards_yellow")),
                        "red_card": get_numeric_value(row.get("cards_red")),
                    }

                    obj, created = PlayerSeasonStats.objects.update_or_create(
                        player=player, season=season, defaults=defaults
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created new stats for player: {row["player_name"]}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Updated existing stats for player: {row["player_name"]}'
                            )
                        )

                except KeyError as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Missing a required column for player {row["player_id"]}: {e}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Error processing row for player {row["player_id"]}: {e}'
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS("Field player stats import completed.")
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'The file "{csv_file_path}" was not found.')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))


# python manage.py import_player_stats WSL_2024_25_COMBINED_PLAYER_STATS.csv --season_id=3
