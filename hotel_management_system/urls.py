from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hotel Management System is live ✅")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
]