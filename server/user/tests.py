from django.contrib.auth.models import User
from django.db import IntegrityError
import pytest

from .models import Profile


@pytest.mark.django_db
class TestProfileModel:
    def test_create_profile_with_defaults(self):
        user = User.objects.create_user(username="ada")
        profile = Profile.objects.create(user=user)
        assert profile.active_team_id == 0
        assert profile.pk is not None

    def test_str_includes_username(self):
        user = User.objects.create_user(username="grace")
        profile = Profile.objects.create(user=user, active_team_id=7)
        assert str(profile) == "Profile(grace)"

    def test_active_team_id_persists(self):
        user = User.objects.create_user(username="linus")
        profile = Profile.objects.create(user=user, active_team_id=42)
        profile.refresh_from_db()
        assert profile.active_team_id == 42

    def test_reverse_accessor(self):
        user = User.objects.create_user(username="margaret")
        Profile.objects.create(user=user)
        assert user.profile.active_team_id == 0

    def test_one_profile_per_user(self):
        user = User.objects.create_user(username="alan")
        Profile.objects.create(user=user)
        with pytest.raises(IntegrityError):
            Profile.objects.create(user=user)

    def test_cascade_delete_removes_profile(self):
        user = User.objects.create_user(username="katherine")
        Profile.objects.create(user=user)
        assert Profile.objects.count() == 1
        user.delete()
        assert Profile.objects.count() == 0
