from django.urls import path

from apps.court.views import ListJudicialApi, ListMatchJudicialApi

urlpatterns = [
    # Neshan
    path("", ListJudicialApi.as_view(), name="list-judicial"),
    path("find", ListMatchJudicialApi.as_view(), name="list-match-judicial"),
]
