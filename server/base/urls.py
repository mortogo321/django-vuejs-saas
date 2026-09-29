from django.urls import path

from .views import health, welcome

urlpatterns = [
    path("", welcome, name="home"),
    path("api/health/", health, name="health"),
]
