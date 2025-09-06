from api.models import Club, League  # Assuming your models are in myapp
from django.db import transaction

league = League.objects.get(pk=2)  # Fetch the league with id 2

clubs_to_create = []
clubs_to_create.append(Club(name="Chelsea", fbref_id="a6a4e67d", league=league))
clubs_to_create.append(Club(name="Arsenal", fbref_id="411b1108", league=league))
clubs_to_create.append(Club(name="Manchester Utd", fbref_id="0bbd83f6", league=league))
clubs_to_create.append(Club(name="Manchester City", fbref_id="9ce68f8a", league=league))
clubs_to_create.append(Club(name="Brighton", fbref_id="fa2752bc", league=league))
clubs_to_create.append(Club(name="Aston Villa", fbref_id="53157aa8", league=league))
clubs_to_create.append(Club(name="Liverpool", fbref_id="00f74a56", league=league))
clubs_to_create.append(Club(name="Everton", fbref_id="c4989550", league=league))
clubs_to_create.append(Club(name="West Ham", fbref_id="52d65cea", league=league))
clubs_to_create.append(Club(name="Leicester City", fbref_id="23bce84e", league=league))
clubs_to_create.append(Club(name="Tottenham", fbref_id="e8e4577c", league=league))
clubs_to_create.append(Club(name="Crystal Palace", fbref_id="78ba1bd4", league=league))

try:
    with transaction.atomic():
        Club.objects.bulk_create(clubs_to_create, ignore_conflicts=True)
        print("Clubs successfully extracted and added to the database.")
except Exception as e:
    print(f"An error occurred: {e}")
