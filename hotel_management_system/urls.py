from django.contrib import admin
from django.urls import path, include
#from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "home.html") #links to the actual website now


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("bookings/", include("bookings.urls")),
    path("accounts/", include("accounts.urls")),
]