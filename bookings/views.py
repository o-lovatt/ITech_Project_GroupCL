from django.shortcuts import render
from bookings.services import show_available_rooms
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from rooms.models import Room
from bookings.models import Booking
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# Create your views here.


def search_rooms(request):
    check_in = request.GET.get("check_in")
    check_out = request.GET.get("check_out")
    list_rooms = []

    if check_in and check_out:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        

        if check_out_date <= check_in_date:
                return render(request, "bookings/search_rooms.html", {
                    "rooms": [],
                    "error": "Check-out must be after check-in.",
                    "check_in": check_in,
                    "check_out": check_out,
                })
        list_rooms = show_available_rooms(check_in_date, check_out_date)

    return render(request, "bookings/search_rooms.html", {"rooms":list_rooms, "check_in":check_in, "check_out":check_out,})

    
@login_required
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

@login_required
def view_bookings(request):
    if request.user.role and request.user.role.role_name.lower() in ["admin", "receptionist"]:#makes it so admin/receptionsit can see all bnookings, guests can only see their own
        bookings = Booking.objects.all()
    else:
        bookings = Booking.objects.filter(user=request.user)
    return render(request, "bookings/view_bookings.html", {"bookings": bookings})


def change_booking_status(request, booking_id, new_status):
    if not request.user.role or request.user.role.role_name not in ["receptionist", "admin"]: #switched this to allow receptionist and admin, for testing ease and also admins would have access in real life usually
        return redirect("view_bookings")

    booking = get_object_or_404(Booking, id = booking_id)
    valid_booking_status = ["checked_in", "checked_out", "cancelled"]

    if new_status in valid_booking_status:
        booking.booking_status = new_status
        booking.save()

    return redirect("view_bookings")