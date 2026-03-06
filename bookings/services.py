from bookings.models import Booking
from rooms.models import Room


def show_available_rooms(check_in_date, check_out_date):
    every_room = Room.objects.all()
    available_rooms = []

    for room in every_room:

        reserved_booking = Booking.objects.filter(room = room, booking_status = ["reserved", "checked_in"])
        overlap = False

        for booking in reserved_booking:
            start_bf_end = check_in_date < booking.check_out_date
            end_af_start = check_out_date > booking.check_in_date

            if start_bf_end and end_af_start:
                overlap = True
                break

        if not overlap:
            available_rooms.append(room)

    return available_rooms