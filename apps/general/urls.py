from django.urls import path

from apps.general.views import GetSearchNeshanApi

urlpatterns = [
    # Neshan
    path("neshan/search", GetSearchNeshanApi.as_view(), name="neshan-search")
]
