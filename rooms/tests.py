from django.test import TestCase
from rooms.models import Room, RoomType
# Create your tests here.


#check created room details are correct
class RoomTypeTest(TestCase):
    def test_creat_roomtype(self):
        
        test_room_type = RoomType.objects.create(room_type_name = "Single", price_per_night = 80.00, max_occupancy = 1)
        
        
        self.assertEqual(test_room_type.room_type_name, "Single")
        self.assertEqual(test_room_type.price_per_night, 80.00)
        self.assertEqual(test_room_type.max_occupancy, 1)

class RoomTest(TestCase):
    def setUp(self):
        self.test_room_type = RoomType.objects.create(room_type_name = "Double", price_per_night = 100.00, max_occupancy = 2)
    def test_create_room(self):
        test_room = Room.objects.create(room_number = "001", room_status = "available", room_type = self.test_room_type)

        self.assertEqual(test_room.room_number, "001")
        self.assertEqual(test_room.room_status, "available")
        self.assertEqual(test_room.room_type, self.test_room_type)