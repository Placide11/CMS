from django.contrib import admin
from .models import Resident, Building, Room, Event

class ResidentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'room', 'is_admin', 'is_staff', 'is_superuser']
    search_fields = ['name', 'email']

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name', 'address']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'building', 'capacity']
    search_fields = ['name']
    list_filter = ['building']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'room']
    search_fields = ['name', 'description']
    list_filter = ['room', 'start_time']

admin.site.register(Resident, ResidentAdmin)
