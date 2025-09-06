from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=70, unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name


class League(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="leagues"
    )
    name = models.CharField(max_length=100)
    total_clubs = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Season(models.Model):
    season = models.CharField(max_length=9)
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name="league_season"
    )

    def __str__(self):
        return self.season


class Club(models.Model):
    name = models.CharField(max_length=300)
    fbref_id = models.CharField(max_length=50, unique=True, db_index=True)

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="clubs")

    def __str__(self):
        return self.name


class ClubSeasonStat(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="season_stats"
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="club_season", db_index=True
    )
    points_won = models.IntegerField()
    league_position = models.IntegerField()
    matches_played = models.IntegerField(null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    draw = models.IntegerField(null=True, blank=True)
    lost = models.IntegerField(null=True, blank=True)
    goals_scored = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    xg_created = models.FloatField(null=True, blank=True)
    xg_conceded = models.FloatField(null=True, blank=True)
    shots = models.IntegerField(null=True, blank=True)
    shots_target = models.IntegerField(null=True, blank=True)
    passes = models.IntegerField(null=True, blank=True)
    passes_comp = models.IntegerField(null=True, blank=True)
    passes_to_final_third = models.IntegerField(null=True, blank=True)
    passes_to_pen_area = models.IntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["club", "season"], name="unique_club_season"
            ),
        ]

    def __str__(self):
        return f"{self.club.name}, {self.season.season}"


class Player(models.Model):
    full_name = models.CharField(max_length=500)
    fbref_id = models.CharField(max_length=100, unique=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="club_player")

    def __str__(self):
        return self.full_name


class PlayerSeasonStats(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_season", db_index=True
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="season_player"
    )
    position = models.CharField(max_length=20, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    matches_played = models.IntegerField(null=True, blank=True)
    minutes_played = models.IntegerField(null=True, blank=True)
    goals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    xg = models.FloatField(null=True, blank=True)
    npxg = models.FloatField(null=True, blank=True)
    prog_carries = models.IntegerField(null=True, blank=True)
    shots_target = models.IntegerField(null=True, blank=True)
    passes_to_final_3rd = models.IntegerField(null=True, blank=True)
    passes_to_pen_area = models.IntegerField(null=True, blank=True)
    shots_creation_action = models.IntegerField(null=True, blank=True)
    tackles = models.IntegerField(null=True, blank=True)
    tackles_won = models.IntegerField(null=True, blank=True)
    interceptions = models.IntegerField(null=True, blank=True)
    touches = models.IntegerField(null=True, blank=True)
    take_ons = models.IntegerField(null=True, blank=True)
    fouls_won = models.IntegerField(null=True, blank=True)
    fouls_commited = models.IntegerField(null=True, blank=True)
    carries_to_final_3rd = models.IntegerField(null=True, blank=True)
    carries_to_pen_area = models.IntegerField(null=True, blank=True)
    yellow_card = models.SmallIntegerField(null=True, blank=True)
    red_card = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player", "season"], name="unique_player_season"
            )
        ]

    def __str__(self):
        return f"{self.player.full_name} {self.position}"


class Goalkeeper(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="goalkeeper_season"
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="season_goalkeeper"
    )
    position = models.CharField(default="GK", max_length=20, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    matches_played = models.IntegerField(null=True, blank=True)
    minutes_played = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    shots_faced = models.IntegerField(null=True, blank=True)
    saves = models.IntegerField(null=True, blank=True)
    save_percentage = models.FloatField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    psxg = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.player.full_name}, GK ({self.season.season})"
