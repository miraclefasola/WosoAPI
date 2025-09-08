from django.contrib import admin
from api.models import *


class PlayerSeasonStatsAdmin(admin.ModelAdmin):
    search_fields=('full_name',)

admin.site.register(Season)
admin.site.register(Country)
admin.site.register(League)
admin.site.register(Club)
admin.site.register(ClubSeasonStat)
admin.site.register(Player)
admin.site.register(PlayerSeasonStats)
admin.site.register(Goalkeeper)
