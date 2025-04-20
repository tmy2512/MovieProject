from django.contrib import admin
from .models import Showtime, Seat

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'screen', 'start_time', 'end_time', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('movie__title', 'theater__name', 'screen__name')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('showtime', 'row', 'number', 'is_available', 'is_reserved')
    list_filter = ('is_available', 'is_reserved')
    search_fields = ('row', 'number')
    ordering = ('showtime', 'row', 'number') 