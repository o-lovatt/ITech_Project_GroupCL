from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError #used for the double booking
# Create your models here.
class Booking(models.Model):

    STATUS = [("reserved", "Reserved"), ("checked_in", "Checked In"), ("checked_out", "Checked Out"), ("cancelled", "Cancelled")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete= models.CASCADE)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    booking_status = models.CharField(max_length= 20, choices = STATUS, default = "reserved")
    #NOTE! DOUBLE BOOKING CAN STILL HAPPEN  update this later
    #^now implemented

    def __str__(self):
        return (f"Booking: {self.id} Room: {self.room}")
    

    def clean(self): #this class controls all the overlapping/impossible date bookings
        #confirm check out is AFTER check in
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out must be after check-in!")
        
        #confirm no other rooms are booked during thse dates
        all_bookings = Booking.objects.filter(room = self.room).exclude(booking_status = "cancelled")#ALL bookings that have already been made
        #now excluding cancelled bookings 

        #this still causes an edge case error, cant save a booking if it's been switched back to cancelled
        #all_bookings = Booking.objects.filter(room = self.room, booking_status = ("reserved" or "checked_in")) #this didnt work
        
        if self.pk:#this should let you update an existing booking 
            all_bookings = all_bookings.exclude(pk = self.pk) 

        for booking in all_bookings:
            start_bf_end = self.check_in_date < booking.check_out_date
            end_af_start = self.check_out_date > booking.check_in_date

            if start_bf_end and end_af_start:
                raise ValidationError("This room has already been booked for these dates.")
            #need to include alllowing booking for a cancelled room
            #^now implemented

#REMEMBER UNIT TESTS!!!!!!!