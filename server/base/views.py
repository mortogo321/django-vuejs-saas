from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def welcome(request: HttpRequest) -> HttpResponse:
    return render(request, "welcome.html")


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})
