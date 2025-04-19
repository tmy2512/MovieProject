from .models import Showtime, Theater, Room
from .serializers import ShowtimeSerializer, TheaterSerializer, RoomSerializer
from datetime import datetime, timedelta
import requests
from django.conf import settings

class ShowtimeService:
    @staticmethod
    def create_showtime(data):
        """Tạo suất chiếu mới"""
        serializer = ShowtimeSerializer(data=data)
        if serializer.is_valid():
            showtime = serializer.save()
            return showtime
        return None

    @staticmethod
    def update_showtime(showtime_id, data):
        """Cập nhật thông tin suất chiếu"""
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            serializer = ShowtimeSerializer(showtime, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            return None
        except Showtime.DoesNotExist:
            return None

    @staticmethod
    def delete_showtime(showtime_id):
        """Xóa suất chiếu"""
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            showtime.delete()
            return True
        except Showtime.DoesNotExist:
            return False

    @staticmethod
    def get_showtime_detail(showtime_id):
        """Lấy chi tiết suất chiếu"""
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            return ShowtimeSerializer(showtime).data
        except Showtime.DoesNotExist:
            return None

    @staticmethod
    def get_showtimes_by_movie(movie_id):
        """Lấy danh sách suất chiếu theo phim"""
        showtimes = Showtime.objects.filter(movie_id=movie_id)
        return ShowtimeSerializer(showtimes, many=True).data

    @staticmethod
    def get_showtimes_by_theater(theater_id):
        """Lấy danh sách suất chiếu theo rạp"""
        showtimes = Showtime.objects.filter(theater_id=theater_id)
        return ShowtimeSerializer(showtimes, many=True).data

    @staticmethod
    def get_showtimes_by_date(date):
        """Lấy danh sách suất chiếu theo ngày"""
        showtimes = Showtime.objects.filter(start_time__date=date)
        return ShowtimeSerializer(showtimes, many=True).data

    @staticmethod
    def get_available_showtimes(movie_id, date):
        """Lấy danh sách suất chiếu còn trống theo phim và ngày"""
        showtimes = Showtime.objects.filter(
            movie_id=movie_id,
            start_time__date=date,
            is_full=False
        )
        return ShowtimeSerializer(showtimes, many=True).data

class TheaterService:
    @staticmethod
    def create_theater(data):
        """Tạo rạp mới"""
        serializer = TheaterSerializer(data=data)
        if serializer.is_valid():
            theater = serializer.save()
            return theater
        return None

    @staticmethod
    def get_all_theaters():
        """Lấy tất cả rạp"""
        theaters = Theater.objects.all()
        return TheaterSerializer(theaters, many=True).data

    @staticmethod
    def get_theater_detail(theater_id):
        """Lấy chi tiết rạp"""
        try:
            theater = Theater.objects.get(id=theater_id)
            return TheaterSerializer(theater).data
        except Theater.DoesNotExist:
            return None

class RoomService:
    @staticmethod
    def create_room(data):
        """Tạo phòng chiếu mới"""
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            room = serializer.save()
            return room
        return None

    @staticmethod
    def get_rooms_by_theater(theater_id):
        """Lấy danh sách phòng chiếu theo rạp"""
        rooms = Room.objects.filter(theater_id=theater_id)
        return RoomSerializer(rooms, many=True).data

    @staticmethod
    def get_room_detail(room_id):
        """Lấy chi tiết phòng chiếu"""
        try:
            room = Room.objects.get(id=room_id)
            return RoomSerializer(room).data
        except Room.DoesNotExist:
            return None 