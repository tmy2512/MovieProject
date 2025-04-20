from rest_framework import serializers
from .models import Showtime, Seat

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_available']

class ShowtimeSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Showtime
        fields = ['id', 'movie_id', 'theater', 'start_time', 'end_time', 'price', 'seats']

class ShowtimeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ['movie_id', 'theater', 'start_time', 'end_time', 'price'] 