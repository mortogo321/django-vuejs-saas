from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Per-user SaaS profile — one row per user, team-scoped later."""

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    active_team_id = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Profile({self.user.username})"
