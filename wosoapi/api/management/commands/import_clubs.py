import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Club


class Command(BaseCommand):
    help = "Import clubs from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The path to the CSV file.")

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs["csv_file"]

        try:
            # Read the CSV file
            df = pd.read_csv(csv_file_path)

            # Counters for tracking imports
            created_count = 0
            updated_count = 0

            for _, row in df.iterrows():
                # Extract club data from the row
                club_data = {
                    "name": row["team_name"],
                    "fbref_id": row["team_id"],
                    # Stadium is not in the CSV, so we leave it blank
                }

                # Update or create the Club
                obj, created = Club.objects.update_or_create(
                    fbref_id=club_data["fbref_id"], defaults=club_data
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Created club: {club_data['name']}")
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"Updated club: {club_data['name']}")
                    )

            # Summary
            self.stdout.write(
                self.style.SUCCESS(
                    f"Import complete! Created: {created_count}, Updated: {updated_count}"
                )
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'The file "{csv_file_path}" was not found.')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))


# python manage.py import_clubs WSL_2025_26_TEAM_STATS.csv
# python manage.py import_clubs Frauen_2025_26_TEAM_STATS.csv
# python manage.py import_clubs Arkema_2025_26_TEAM_STATS.csv
# python manage.py import_clubs NWSL_2025_26_TEAM_STATS.csv
#python manage.py import_clubs LigaF_2025_26_TEAM_STATS.csv