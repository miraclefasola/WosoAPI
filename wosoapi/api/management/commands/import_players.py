import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Club, Player


class Command(BaseCommand):
    help = "Imports player data from a specified CSV file for a given club."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The path to the CSV file.")
        parser.add_argument(
            "--club_fbref_id",
            type=str,
            required=True,
            help="The fbref_id of the club to import players for.",
        )

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csv_file"]
        club_fbref_id = kwargs["club_fbref_id"]

        try:
            # Find the Club object by its fbref_id
            club = Club.objects.get(fbref_id=club_fbref_id)
        except Club.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Club with fbref_id "{club_fbref_id}" does not exist.'
                )
            )
            return

        try:
            self.stdout.write(f"Reading data from {csv_file_path}...")
            df = pd.read_csv(csv_file_path)

            # Filter the DataFrame to get only the players for the specified club
            players_df = df[df["team_id"] == club_fbref_id].drop_duplicates(
                subset=["player_id"]
            )

            if players_df.empty:
                self.stdout.write(
                    self.style.WARNING(
                        f'No players found for club with fbref_id "{club_fbref_id}" in the CSV.'
                    )
                )
                return

            players_to_create = []
            for _, row in players_df.iterrows():
                # Map CSV columns to Player model fields
                full_name = row["player_name"]
                fbref_id = row["player_id"]

                players_to_create.append(
                    Player(full_name=full_name, fbref_id=fbref_id, club=club)
                )

            with transaction.atomic():
                Player.objects.bulk_create(players_to_create, ignore_conflicts=True)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{len(players_to_create)} players successfully imported for {club.name}."
                    )
                )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'The file "{csv_file_path}" was not found.')
            )
        except KeyError as e:
            self.stdout.write(
                self.style.ERROR(f"Missing a required column in the CSV file: {e}")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))


# python manage.py import_players WSL_2024_25_ALL_PLAYER_STATS_20250821_102053.csv --club_fbref_id=78ba1bd4
