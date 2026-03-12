from django.contrib import admin
from .models import Booking
# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "check_in_date", "check_out_date", "booking_status")
#^updated so bookings show in the admin panel too
admin.site.register(Booking, BookingAdmin)
