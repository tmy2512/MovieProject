from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'movie_id', 'showtime', 'seats', 
                 'total_price', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('movie_id', 'showtime', 'seats', 'total_price') 