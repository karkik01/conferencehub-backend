from django.contrib import admin
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location', 'is_available')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date', 'start_time', 'end_time', 'status')
