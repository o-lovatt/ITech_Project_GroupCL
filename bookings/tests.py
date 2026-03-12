from django.test import TestCase
from django.contrib.auth import get_user_model
from rooms.models import Room, RoomType
from bookings.models import Booking
from django.core.exceptions import ValidationError
from datetime import date
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
        test_booking1 = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10))

        #overlappingbooking
        test_booking2 = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10))

        with self.assertRaises(ValidationError):
            test_booking2.clean()
        


    def test_cancelled_booking_excluded(self):
        #cancelled
        test_cancelled_booking = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10), booking_status = "cancelled")#if this is reserved, the test fails
        #reserved
        test_reserved_booking = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10), booking_status = "reserved")

        test_reserved_booking.clean()
        test_reserved_booking.save()
        self.assertEqual(Booking.objects.count(), 2) 


    def test_available_rooms(self):
        #available 
        available_room = Booking.objects.create(user = self.user, room = self.room, check_in_date = date(2026, 3, 3), check_out_date = date(2026, 3, 10), booking_status = "available")
            #not sure how to structure this fully ?? will need to properly add later when checking available rooms is possible



#CHECK ALL OF THESE ARE ACTUALLY OK!!!
    