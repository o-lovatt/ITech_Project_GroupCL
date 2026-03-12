from django.test import TestCase
from django.contrib.auth import get_user_model
from rooms.models import Room, RoomType
from bookings.models import Booking
from django.core.exceptions import ValidationError
from datetime import date
from accounts.models import Role
# Create your tests here
user_model = get_user_model()

class BookeingTest(TestCase):
    
    def setUp(self):
        self.user = user_model.objects.create_user(username = "ollie", password = "password")
        self.room_type = RoomType.objects.create(room_type_name = "Family", price_per_night = 120.00, max_occupancy = 4)
        self.room = Room.objects.create(room_number = "002", room_status = "available", room_type = self.room_type)

    #test booking works at all
    def test_valid_booking(self):#CHECK THIS AGAIN
        test_booking = Booking(user = self.user, room = self.room, check_in_date = date(2026, 3, 2), check_out_date = date(2026, 3, 3))
        test_booking.clean()#.clean runs validation like overlapping etc
        test_booking.save()#.save save the object to the test database
        self.assertEqual(Booking.objects.count(), 1)   #this test is failing?? AssertionError: 0 != 1      
        #^^ now fixed, needed to add 'date' to   (2026, 3, 2)          



    #test check out date can't come befor check in 
    def test_checkout_date(self):
        test_booking = Booking(user = self.user, room = self.room, check_in_date = date(2026, 3, 2), check_out_date = date(2026, 3, 1))
        with self.assertRaises(ValidationError):
            test_booking.clean()
            test_booking.save()
        


        
    #test bookings can't overlap
    def test_booking_overlap(self):
        #original booking
        Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10))

        #overlappingbooking
        overlapping_booking = Booking(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10))

        with self.assertRaises(ValidationError):
            overlapping_booking.clean()

            #THIS IS FAILING
            #fixed - renamed test_booking2 to overlapping_booking
        


    def test_cancelled_booking_excluded(self):
        #cancelled
        test_cancelled_booking = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10), booking_status = "cancelled")#if this is reserved, the test fails
        #reserved
        test_reserved_booking = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10), booking_status = "reserved")

        test_reserved_booking.clean()
        test_reserved_booking.save()
        self.assertEqual(Booking.objects.count(), 2) 


    def test_available_rooms(self):
        available_room = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10), booking_status = "reserved")
            #not sure how to structure this fully ?? will need to properly add later when checking available rooms is possible
            #THIS IS FAILING
            #^^ fixed - 'available' wasn;t a valid booking status



    def test_search_bookings_page(self):
        response = self.client.get("/bookings/search/")
        self.assertEqual(response.status_code, 200)



    def test_view_bookings_page(self):
        self.client.force_login(self.user)
        response = self.client.get("/bookings/view_bookings/")
        self.assertEqual(response.status_code, 200)


class BookingViewTest(TestCase):
    def setUp(self):
        #create roles
        self.admin_role = Role.objects.create(role_name = "admin")
        self.receptionist_role = Role.objects.create(role_name = "receptionist")
        self.guest_role = Role.objects.create(role_name = "guest")
        #create users
        self.admin_user = user_model.objects.create_user(username = "admin_user", password = "password", role = self.admin_role)
        self.receptionist_user = user_model.objects.create_user(username = "receptionist_user", password = "password", role = self.receptionist_role)
        self.guest_user = user_model.objects.create_user(username = "guest_user", password = "password", role = self.guest_role)
        #create room type
        self.room_type = RoomType.objects.create(room_type_name = "Single", price_per_night = 80.00, max_occupancy = 1)
        #create room
        self.room = Room.objects.create(room_number = "101", room_status = "available", room_type = self.room_type)
        #create booking
        self.booking = Booking.objects.create(user = self.guest_user, room = self.room, check_in_date = date(2026, 4, 10), check_out_date = date(2026, 4, 17), booking_status = "reserved")


    def guest_cant_change_booking_status(self):
        self.client.force_login(self.guest_user)
        response = self.client.get(f"/bookings/change_booking_status/{self.booking.id}/checked_in/")
        self.booking.refresh_from_db()#refresh for latest booking

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.booking.booking_status, "reserved")

#tests to add:
# - booking creation redirects correctly
# - changing booking status works for allowed users
# - receptionist/admin can change a booking to checked_in a normal user cannot


#CHECK ALL OF THESE ARE ACTUALLY OK!!!
#all currently pass
    