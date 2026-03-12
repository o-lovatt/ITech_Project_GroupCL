from django.urls import path
from . import views


urlpatterns = [path("search/", views.search_rooms, name = "search_rooms"),
               path("create/<int:room_id>/", views.create_booking, name="create_booking"),
               path("view_bookings/", views.view_bookings, name="view_bookings"),
               path("change_booking_status/<int:booking_id>/<str:new_status>/", views.change_booking_status, name = "change_booking_status"),]