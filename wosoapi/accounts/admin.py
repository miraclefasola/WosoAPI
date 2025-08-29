from django.contrib import admin

# Register your models here.
from django.contrib import admin
from accounts.models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]


admin.site.register(CustomUser, UserAdmin)
