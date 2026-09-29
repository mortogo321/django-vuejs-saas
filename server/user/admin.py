from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "active_team_id")
    list_select_related = ("user",)
    search_fields = ("user__username",)
