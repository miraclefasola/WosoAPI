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
        return f"{self.name}, {self.country.code}"
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"], name="unique_country_name"
            ),
        ]


class Season(models.Model):
    season = models.CharField(max_length=9)
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name="league_season"
    )

    def __str__(self):
        return f"{self.season} {self.league.name}" 
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["league", "season"], name="unique_league_season"
            ),
        ]


class Club(models.Model):
    name = models.CharField(max_length=300, unique=True)
    fbref_id = models.CharField(max_length=50, unique=True, db_index=True)
    stadium=models.CharField(max_length=200, blank=True, null=True)

    

    def __str__(self):
        return self.name


class ClubSeasonStat(models.Model):
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="season_stats"
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="club_season", db_index=True
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="clubs")
    
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
    shots_allowed = models.IntegerField(null=True, blank=True)
    shots_target_allowed = models.IntegerField(null=True, blank=True)
    attempted_passes_against = models.IntegerField(null=True, blank=True)
    comp_passes_allowed = models.IntegerField(null=True, blank=True)
    passes_to_final_third_allowed = models.IntegerField(null=True, blank=True)
    passes_to_pen_area_allowed = models.IntegerField(null=True, blank=True)

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
    nationality=models.CharField(max_length=50, null=True, blank=True)
    age=models.SmallIntegerField(null=True,blank=True)

    def __str__(self):
        return self.full_name


class PlayerSeasonStats(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player_season", db_index=True
    )
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name="season_player"
    )
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="player_clubstats"
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_of_player")
    position = models.CharField(max_length=20, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    matches_played = models.IntegerField(null=True, blank=True)
    minutes_played = models.IntegerField(null=True, blank=True)
    matches_completed=models.IntegerField(null=True, blank=True)
    matches_substituted=models.IntegerField(null=True, blank=True)
    unused_sub=models.IntegerField(null=True, blank=True)
    goals = models.IntegerField(null=True, blank=True)
    assists = models.IntegerField(null=True, blank=True)
    xg = models.FloatField(null=True, blank=True)
    npxg = models.FloatField(null=True, blank=True)
    xg_performance=models.FloatField(null=True, blank=True)
    npxg_performance= models.FloatField(null=True, blank=True)
    prog_carries = models.IntegerField(null=True, blank=True)
    prog_carries_final_3rd= models.IntegerField(null=True, blank=True)
    prog_passes=models.IntegerField(null=True, blank=True)
    shots_target = models.IntegerField(null=True, blank=True)
    passes_to_final_3rd = models.IntegerField(null=True, blank=True)
    passes_to_pen_area = models.IntegerField(null=True, blank=True)
    pass_switches=models.IntegerField(null=True, blank=True)
    through_ball=models.IntegerField(null=True, blank=True)
    shots_creation_action = models.IntegerField(null=True, blank=True)
    offsides=models.IntegerField(null=True, blank=True)
    pen_won=models.IntegerField(null=True, blank=True)
    pen_conceded=models.IntegerField(null=True, blank=True)
    tackles = models.IntegerField(null=True, blank=True)
    ball_recoveries=models.IntegerField(null=True, blank=True)
    aerial_duels_won=models.IntegerField(null=True, blank=True)
    aerial_duels_lost=models.IntegerField(null=True, blank=True)
    blocks=models.IntegerField(null=True, blank=True)
    tackles_won = models.IntegerField(null=True, blank=True)
    interceptions = models.IntegerField(null=True, blank=True)
    touches = models.IntegerField(null=True, blank=True)
    dispossessed=models.IntegerField(null=True, blank=True)
    miscontrols=models.IntegerField(null=True, blank=True)
    take_ons = models.IntegerField(null=True, blank=True)
    take_ons_won= models.IntegerField(null=True, blank=True)
    fouls_won = models.IntegerField(null=True, blank=True)
    fouls_committed = models.IntegerField(null=True, blank=True)
    carries_to_final_3rd = models.IntegerField(null=True, blank=True)
    carries_to_pen_area = models.IntegerField(null=True, blank=True)
    yellow_card = models.SmallIntegerField(null=True, blank=True)
    red_card = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player","season","club"], name="unique_player_season_club"
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
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE, related_name="goalkeeper_clubstats"
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="league_of_goalkeeper")
    position = models.CharField(default="GK", max_length=20)
    age = models.SmallIntegerField(null=True, blank=True)
    matches_played = models.IntegerField(null=True, blank=True)
    minutes_played = models.IntegerField(null=True, blank=True)
    goals_conceded = models.IntegerField(null=True, blank=True)
    shots_faced = models.IntegerField(null=True, blank=True)
    saves = models.IntegerField(null=True, blank=True)
    save_percentage = models.FloatField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    psxg = models.FloatField(null=True, blank=True)
    psxg_performance=models.FloatField(null=True,blank=True)
    pen_saved=models.IntegerField(null=True, blank=True)
    passes=models.IntegerField(null=True, blank=True)
    crosses_stopped=models.IntegerField(null=True, blank=True)
    sweeper_action=models.IntegerField(null=True, blank=True)
    sweeper_action_per90=models.FloatField(null=True, blank=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["player", "season","club"], name="unique_goalkeeper_season_club"
            )
        ]


    def __str__(self):
        return f"{self.player.full_name}, GK ({self.season.season})"
