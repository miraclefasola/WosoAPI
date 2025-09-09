import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Player  # Assuming your Player model is in api/models.py
import numpy as np

class Command(BaseCommand):
    help = "Imports or updates player data from a given CSV file."

    def add_arguments(self, parser):
        """Adds a command-line argument to specify the CSV file path."""
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing player data.')

    def handle(self, *args, **kwargs):
        """The main logic for the management command."""
        csv_file_path = kwargs['csv_file']

        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)
            
            # Check for the existence of required columns
            required_cols = ['player_name', 'player_id', 'nationality', 'age']
            if not all(col in df.columns for col in required_cols):
                self.stdout.write(self.style.ERROR(
                    f"CSV file must contain the following columns: {', '.join(required_cols)}"
                ))
                return

            # Counters for tracking the import process
            created_count = 0
            updated_count = 0

            # Iterate through each row of the DataFrame
            for _, row in df.iterrows():
                try:
                    # Clean and prepare the data from the row
                    # Pandas might read empty cells as NaN, so we handle that for age and nationality
                    age = int(row['age']) if pd.notna(row['age']) else None
                    nationality = row['nationality'] if pd.notna(row['nationality']) else None

                    # Use update_or_create to handle new and existing players
                    # The 'fbref_id' is used as the unique identifier to prevent duplicates.
                    player, created = Player.objects.update_or_create(
                        fbref_id=row['player_id'],
                        defaults={
                            'full_name': row['player_name'],
                            'nationality': nationality,
                            'age': age,
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Created player: {player.full_name} ({player.fbref_id})")
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"Updated player: {player.full_name} ({player.fbref_id})")
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"Skipping row due to an error for player ID {row['player_id']}: {e}"
                    ))

            # Final summary
            self.stdout.write(self.style.SUCCESS(
                f"\nPlayer import complete! Created: {created_count}, Updated: {updated_count}"
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f'The file "{csv_file_path}" was not found.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

#python manage.py import_players WSL_2024_25_ALL_PLAYER_STATS_20250821_102053.csv