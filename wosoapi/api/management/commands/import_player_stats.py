import pandas as pd
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from api.models import Player, Club, Season, League, PlayerSeasonStats
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
            
            # Check for the existence of required columns
            required_cols = [
                'player_id', 'team_id', 'position', 'age', 'games', 'minutes', 'goals', 'assists',
                'xg', 'npxg', 'progressive_carries', 'progressive_passes', 'shots_on_target',
                'passes_into_final_third', 'passes_into_penalty_area', 'passes_switches',
                'through_balls', 'sca', 'offsides', 'pens_won', 'pens_conceded', 'tackles',
                'ball_recoveries', 'aerials_won', 'aerials_lost', 'blocks', 'tackles_won',
                'interceptions', 'touches', 'dispossessed', 'miscontrols', 'take_ons', 'fouled',
                'fouls', 'carries_into_final_third', 'carries_into_penalty_area', 'cards_yellow',
                'cards_red', 'games_complete', 'games_subs', 'unused_subs'
            ]
            if not all(col in df.columns for col in required_cols):
                self.stdout.write(self.style.ERROR(
                    f"CSV file must contain all required columns for PlayerSeasonStats."
                ))
                return

            # Counters for tracking the import process
            created_count = 0
            updated_count = 0

            # Iterate through each row of the DataFrame
            for _, row in df.iterrows():
                # Skip goalkeepers
                if row['position'] == 'GK':
                    self.stdout.write(self.style.NOTICE(f"Skipping goalkeeper: {row['player_id']}"))
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
                    data = {
                        'position': row['position'] if pd.notna(row['position']) else None,
                        'age': age,
                        'matches_played': int(float(str(row['games']).replace(',', ''))) if pd.notna(row['games']) else 0,
                        'minutes_played': int(float(str(row['minutes']).replace(',', ''))) if pd.notna(row['minutes']) else 0,
                        'matches_completed': int(float(str(row['games_complete']).replace(',', ''))) if pd.notna(row['games_complete']) else 0,
                        'matches_substituted': int(float(str(row['games_subs']).replace(',', ''))) if pd.notna(row['games_subs']) else 0,
                        'unused_sub': int(float(str(row['unused_subs']).replace(',', ''))) if pd.notna(row['unused_subs']) else 0,
                        'goals': int(float(str(row['goals']).replace(',', ''))) if pd.notna(row['goals']) else 0,
                        'assists': int(float(str(row['assists']).replace(',', ''))) if pd.notna(row['assists']) else 0,
                        'xg': float(str(row['xg']).replace(',', '')) if pd.notna(row['xg']) else 0.0,
                        'npxg': float(str(row['npxg']).replace(',', '')) if pd.notna(row['npxg']) else 0.0,
                        'xg_performance': (float(str(row['goals']).replace(',', '')) - float(str(row['xg']).replace(',', ''))) if pd.notna(row['goals']) and pd.notna(row['xg']) else 0.0,
                        'npxg_performance': (float(str(row['goals']).replace(',', '')) - float(str(row['npxg']).replace(',', ''))) if pd.notna(row['goals']) and pd.notna(row['npxg']) else 0.0,
                        'prog_carries': int(float(str(row['progressive_carries']).replace(',', ''))) if pd.notna(row['progressive_carries']) else 0,
                        'prog_carries_final_3rd': int(float(str(row['carries_into_final_third']).replace(',', ''))) if pd.notna(row['carries_into_final_third']) else 0,
                        'prog_passes': int(float(str(row['progressive_passes']).replace(',', ''))) if pd.notna(row['progressive_passes']) else 0,
                        'shots_target': int(float(str(row['shots_on_target']).replace(',', ''))) if pd.notna(row['shots_on_target']) else 0,
                        'passes_to_final_3rd': int(float(str(row['passes_into_final_third']).replace(',', ''))) if pd.notna(row['passes_into_final_third']) else 0,
                        'passes_to_pen_area': int(float(str(row['passes_into_penalty_area']).replace(',', ''))) if pd.notna(row['passes_into_penalty_area']) else 0,
                        'pass_switches': int(float(str(row['passes_switches']).replace(',', ''))) if pd.notna(row['passes_switches']) else 0,
                        'through_ball': int(float(str(row['through_balls']).replace(',', ''))) if pd.notna(row['through_balls']) else 0,
                        'shots_creation_action': int(float(str(row['sca']).replace(',', ''))) if pd.notna(row['sca']) else 0,
                        'offsides': int(float(str(row['offsides']).replace(',', ''))) if pd.notna(row['offsides']) else 0,
                        'pen_won': int(float(str(row['pens_won']).replace(',', ''))) if pd.notna(row['pens_won']) else 0,
                        'pen_conceded': int(float(str(row['pens_conceded']).replace(',', ''))) if pd.notna(row['pens_conceded']) else 0,
                        'tackles': int(float(str(row['tackles']).replace(',', ''))) if pd.notna(row['tackles']) else 0,
                        'ball_recoveries': int(float(str(row['ball_recoveries']).replace(',', ''))) if pd.notna(row['ball_recoveries']) else 0,
                        'aerial_duels_won': int(float(str(row['aerials_won']).replace(',', ''))) if pd.notna(row['aerials_won']) else 0,
                        'aerial_duels_lost': int(float(str(row['aerials_lost']).replace(',', ''))) if pd.notna(row['aerials_lost']) else 0,
                        'blocks': int(float(str(row['blocks']).replace(',', ''))) if pd.notna(row['blocks']) else 0,
                        'tackles_won': int(float(str(row['tackles_won']).replace(',', ''))) if pd.notna(row['tackles_won']) else 0,
                        'interceptions': int(float(str(row['interceptions']).replace(',', ''))) if pd.notna(row['interceptions']) else 0,
                        'touches': int(float(str(row['touches']).replace(',', ''))) if pd.notna(row['touches']) else 0,
                        'dispossessed': int(float(str(row['dispossessed']).replace(',', ''))) if pd.notna(row['dispossessed']) else 0,
                        'miscontrols': int(float(str(row['miscontrols']).replace(',', ''))) if pd.notna(row['miscontrols']) else 0,
                        'take_ons': int(float(str(row['take_ons']).replace(',', ''))) if pd.notna(row['take_ons']) else 0,
                        'fouls_won': int(float(str(row['fouled']).replace(',', ''))) if pd.notna(row['fouled']) else 0,
                        'fouls_committed': int(float(str(row['fouls']).replace(',', ''))) if pd.notna(row['fouls']) else 0,
                        'carries_to_final_3rd': int(float(str(row['carries_into_final_third']).replace(',', ''))) if pd.notna(row['carries_into_final_third']) else 0,
                        'carries_to_pen_area': int(float(str(row['carries_into_penalty_area']).replace(',', ''))) if pd.notna(row['carries_into_penalty_area']) else 0,
                        'yellow_card': int(float(str(row['cards_yellow']).replace(',', ''))) if pd.notna(row['cards_yellow']) else 0,
                        'red_card': int(float(str(row['cards_red']).replace(',', ''))) if pd.notna(row['cards_red']) else 0,
                    }

                    # Use update_or_create to handle new and existing stats entries.
                    # This respects the unique constraint on (player, season, club).
                    obj, created = PlayerSeasonStats.objects.update_or_create(
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
                f"\nPlayer season stats import complete! Created: {created_count}, Updated: {updated_count}"
            ))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f'The file "{csv_file_path}" was not found.'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

#python manage.py import_player_stats WSL_2025_26_ALL_PLAYER_STATS.csv --season-id=2 --league-id=1