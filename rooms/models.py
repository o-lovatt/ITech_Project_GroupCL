from django.db import models

# Create your models here.

class RoomType(models.Model):



    room_type_name = models.CharField(max_length= 10, unique = True)
    price_per_night = models.DecimalField(max_digits= 5, decimal_places= 2)
    max_occupancy = models.IntegerField()

    def __str__(self):
        return self.room_type_name


class Room(models.Model):

    STATUS = [("available", "Available"), ("occupided", "Occupied"), ("maintenence", "Maintenance")]
    #this isnt working needs to be a tuple ??
    #FIXED

    room_no = models.CharField(max_length = 3, unique = True)

    room_status = models.CharField(max_length = 20, choices= STATUS, default = "Available")
    room_type = models.ForeignKey(RoomType, on_delete = models.CASCADE)
    

    def __str__(self):
        return (f"Room: {self.room_no}")


        