import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from api.models import Player, Club, Season, League, Goalkeeper
import numpy as np

class Command(BaseCommand):
    help = "Imports or updates player season stats from a given CSV file."

    def add_arguments(self, parser):
        """Adds command-line arguments to specify the CSV file, season ID, and league ID."""
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing player data.')
        parser.add_argument('--season-id', type=int, required=True, help='The database ID of the season (e.g., 1).')
        parser.add_argument('--league-id', type=int, required=True, help='The database ID of the league (e.g., 189).')

    def handle(self, *args, **kwargs):
        """The main logic for the management command."""
        csv_file_path = kwargs['csv_file']
        season_id = kwargs['season_id']
        league_id = kwargs['league_id']

        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)
            
            # Look up the Season and League objects by their IDs
            try:
                season = Season.objects.get(id=season_id)
            except Season.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Season with ID {season_id} does not exist. Please check the ID and try again."))
                return

            try:
                league = League.objects.get(id=league_id)
            except League.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"League with ID {league_id} does not exist. Please check the ID and try again."))
                return
            
            # Check for the existence of required columns for goalkeepers
            required_cols = [
                'player_id', 'team_id', 'position', 'age', 'gk_games', 'gk_minutes', 'gk_goals_against', 
                'gk_shots_on_target_against', 'gk_saves', 'gk_save_pct', 'gk_clean_sheets', 'gk_psxg', 
                'gk_psxg_net', 'gk_pens_saved', 'gk_passes', 'gk_crosses_stopped', 'gk_def_actions_outside_pen_area', 'gk_def_actions_outside_pen_area_per90'
            ]
            
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                self.stdout.write(self.style.ERROR(
                    f"CSV file is missing the following required columns for Goalkeeper stats: {', '.join(missing_cols)}"
                ))
                return

            # Counters for tracking the import process
            created_count = 0
            updated_count = 0

            # Iterate through each row of the DataFrame
            for _, row in df.iterrows():
                # Skip outfield players
                if row['position'] != 'GK':
                    self.stdout.write(self.style.NOTICE(f"Skipping outfield player: {row['player_id']}"))
                    continue

                try:
                    # Look up the Player and Club objects using their fbref_id
                    player = Player.objects.get(fbref_id=row['player_id'])
                    club = Club.objects.get(fbref_id=row['team_id'])

                    # The age column contains values in the format 'YY-DDD'.
                    # This code splits the string at the hyphen and takes the year part.
                    # It also handles cases where age is a float or is missing.
                    try:
                        age_str = str(row['age'])
                        if pd.notna(row['age']) and '-' in age_str:
                            age = int(age_str.split('-')[0])
                        elif pd.notna(row['age']):
                            age = int(float(age_str))
                        else:
                            age = None
                    except (ValueError, TypeError):
                        age = None

                    # Prepare data, handling potential NaN values, commas, and decimals in numbers
                    goals_conceded = int(float(str(row['gk_goals_against']).replace(',', ''))) if pd.notna(row['gk_goals_against']) else 0
                    psxg = float(str(row['gk_psxg']).replace(',', '')) if pd.notna(row['gk_psxg']) else 0.0

                    data = {
                        'position': 'GK',
                        'age': age,
                        'matches_played': int(float(str(row['gk_games']).replace(',', ''))) if pd.notna(row['gk_games']) else 0,
                        'minutes_played': int(float(str(row['gk_minutes']).replace(',', ''))) if pd.notna(row['gk_minutes']) else 0,
                        'goals_conceded': goals_conceded,
                        'shots_faced': int(float(str(row['gk_shots_on_target_against']).replace(',', ''))) if pd.notna(row['gk_shots_on_target_against']) else 0,
                        'saves': int(float(str(row['gk_saves']).replace(',', ''))) if pd.notna(row['gk_saves']) else 0,
                        'save_percentage': float(str(row['gk_save_pct']).replace(',', '')) if pd.notna(row['gk_save_pct']) else 0.0,
                        'clean_sheets': int(float(str(row['gk_clean_sheets']).replace(',', ''))) if pd.notna(row['gk_clean_sheets']) else 0,
                        'psxg': psxg,
                        'psxg_performance': float(str(row['gk_psxg_net']).replace(',', '')) if pd.notna(row['gk_psxg_net']) else 0.0,
                        'pen_saved': int(float(str(row['gk_pens_saved']).replace(',', ''))) if pd.notna(row['gk_pens_saved']) else 0,
                        'passes': int(float(str(row['gk_passes']).replace(',', ''))) if pd.notna(row['gk_passes']) else 0,
                        'crosses_stopped': int(float(str(row['gk_crosses_stopped']).replace(',', ''))) if pd.notna(row['gk_crosses_stopped']) else 0,
                        'sweeper_action': int(float(str(row['gk_def_actions_outside_pen_area']).replace(',', ''))) if pd.notna(row['gk_def_actions_outside_pen_area']) else 0,
                        'sweeper_action_per90': float(str(row['gk_def_actions_outside_pen_area_per90']).replace(',', '')) if pd.notna(row['gk_def_actions_outside_pen_area_per90']) else 0.0,
                    }

                    # Use update_or_create to handle new and existing stats entries.
                    obj, created = Goalkeeper.objects.update_or_create(
                        player=player,
                        season=season,
                        club=club,
                        league=league,
                        defaults=data
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Created stats for {player.full_name} at {club.name}")
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(f"Updated stats for {player.full_name} at {club.name}")
                        )

                except Player.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"Skipping row: Player with fbref_id '{row['player_id']}' not found in the database. Please run the import_players command first."
                    ))
                except Club.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"Skipping row: Club with fbref_id '{row['team_id']}' not found in the database. Please run the import_clubs command first."
                    ))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(
                        f"Integrity Error for player ID {row['player_id']} at club ID {row['team_id']}: {e}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"An unexpected error occurred while processing row for player ID {row['player_id']}: {e}"
                    ))

            # Final summary
            self.stdout.write(self.style.SUCCESS(
                f"\nGoalkeeper season stats import complete! Created: {created_count}, Updated: {updated_count}"
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f'The file "{csv_file_path}" was not found.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))


#python manage.py import_goalkeeper_stats WSL_2025_26_ALL_PLAYER_STATS.csv --season-id=2 --league-id=1