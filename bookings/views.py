from django.shortcuts import render
from bookings.services import show_available_rooms
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from rooms.models import Room
from bookings.models import Booking
from django.core.exceptions import ValidationError
# Create your views here.


def search_rooms(request):
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    list_rooms = []

    if check_in and check_out:
        check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        list_rooms = show_available_rooms(check_in, check_out)

    return render(request, "bookings/search_rooms.html", {"rooms":list_rooms})


def create_booking(request, room_id):
    room = get_object_or_404(Room, id = room_id)

    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")


    if not check_in or not check_out: #this was breaking it, needed 'not'
        return redirect("search_rooms")
    
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
    
    try: ##adding error handling for double bookings
        Booking.objects.create(user = request.user, room = room, check_in_date = check_in_date, check_out_date = check_out_date, booking_status = "reserved")

        return redirect("view_bookings")
#for some reason double bookings are allowed when made in the view?
#^^sort of fixed - now redirects to error page

    except ValidationError:
        return render(request, "bookings/booking_error.html", {"error": "This room has already been booked for the selected dates."})
    #remember to create a html for the error page ^^

def view_bookings(request):
    bookings = Booking.objects.filter(user = request.user)
    return render(request, "bookings/view_bookings.html", {"bookings": bookings})