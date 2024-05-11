from django.http import HttpRequest
from django.shortcuts import render


def welcome(request: HttpRequest) -> render:
    return render(request, "welcome.html")
