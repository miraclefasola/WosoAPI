import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Club, Season, League, ClubSeasonStat

class Command(BaseCommand):
    help = "Import club season stats from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="The path to the CSV file.")
        parser.add_argument(
            "--season_id",
            type=int,
            required=True,
            help="The ID of the season to associate the stats with.",
        )
        parser.add_argument(
            "--league_id",
            type=int,
            required=True,
            help="The ID of the league to associate the stats with.",
        )

def handle(self, *args, **kwargs):
    csv_file_path = kwargs["csv_file"]
    season_id = kwargs["season_id"]
    league_id = kwargs["league_id"]

    try:
        # Get the Season and League objects
        season = Season.objects.get(pk=season_id)
        league = League.objects.get(pk=league_id)
    except (Season.DoesNotExist, League.DoesNotExist) as e:
        self.stdout.write(self.style.ERROR(f"{e}"))
        return

    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
        # Counters for tracking imports
        created_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            try:
                # Get the club
                club = Club.objects.get(fbref_id=row['team_id'])
                
                
                stats_data = {
                    'points_won': row['points'],
                    'league_position': row['rank'],
                    'matches_played': row.get('games'),
                    'win': row.get('wins'),
                    'draw': row.get('ties'),
                    'lost': row.get('losses'),
                    'goals_scored': row.get('goals_for'),
                    'goals_conceded': row.get('goals_against'),
                    'xg_created': row.get('xg_for'),
                    'xg_conceded': row.get('xg_against'),
                    'shots_allowed': row.get('shots'),
                    'shots_target_allowed': row.get('shots_on_target'),
                    'attempted_passes_against': row.get('passes'),
                    'comp_passes_allowed': row.get('passes_completed'),
                    'passes_to_final_third_allowed': row.get('passes_into_final_third'),
                    'passes_to_pen_area_allowed': row.get('passes_into_penalty_area'),
                }
                
                # Update or create the ClubSeasonStat record
                obj, created = ClubSeasonStat.objects.update_or_create(
                    club=club,
                    season=season,
                    defaults={
                        'league': league,
                        **stats_data
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"Created stats for: {club.name}")
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f"Updated stats for: {club.name}")
                    )
                
            except Club.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"Club with fbref_id {row['team_id']} does not exist")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error processing {row['team_name']}: {e}")
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
        self.stdout.write(
            self.style.ERROR(f"An error occurred: {e}")
        )

#python manage.py import_club_season_stats WSL_2025_26_TEAM_STATS.csv --season_id=2 --league_id=1