from .models import Booking, Ticket, Seat
from .serializers import BookingSerializer, TicketSerializer, SeatSerializer
from datetime import datetime
import requests
from django.conf import settings

class BookingService:
    @staticmethod
    def create_booking(data):
        """Tạo đặt vé mới"""
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            return booking
        return None

    @staticmethod
    def update_booking(booking_id, data):
        """Cập nhật thông tin đặt vé"""
        try:
            booking = Booking.objects.get(id=booking_id)
            serializer = BookingSerializer(booking, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            return None
        except Booking.DoesNotExist:
            return None

    @staticmethod
    def delete_booking(booking_id):
        """Xóa đặt vé"""
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return True
        except Booking.DoesNotExist:
            return False

    @staticmethod
    def get_booking_detail(booking_id):
        """Lấy chi tiết đặt vé"""
        try:
            booking = Booking.objects.get(id=booking_id)
            return BookingSerializer(booking).data
        except Booking.DoesNotExist:
            return None

    @staticmethod
    def get_bookings_by_user(user_id):
        """Lấy danh sách đặt vé theo người dùng"""
        bookings = Booking.objects.filter(user_id=user_id)
        return BookingSerializer(bookings, many=True).data

    @staticmethod
    def get_bookings_by_showtime(showtime_id):
        """Lấy danh sách đặt vé theo suất chiếu"""
        bookings = Booking.objects.filter(showtime_id=showtime_id)
        return BookingSerializer(bookings, many=True).data

    @staticmethod
    def check_seat_availability(showtime_id, seat_id):
        """Kiểm tra ghế còn trống không"""
        try:
            seat = Seat.objects.get(id=seat_id)
            booking = Booking.objects.filter(
                showtime_id=showtime_id,
                seats=seat
            ).first()
            return booking is None
        except Seat.DoesNotExist:
            return False

    @staticmethod
    def calculate_total_price(showtime_id, seat_ids):
        """Tính tổng giá vé"""
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            seats = Seat.objects.filter(id__in=seat_ids)
            total_price = showtime.price * len(seats)
            return total_price
        except Showtime.DoesNotExist:
            return None

class TicketService:
    @staticmethod
    def create_ticket(data):
        """Tạo vé mới"""
        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            ticket = serializer.save()
            return ticket
        return None

    @staticmethod
    def get_tickets_by_booking(booking_id):
        """Lấy danh sách vé theo đặt vé"""
        tickets = Ticket.objects.filter(booking_id=booking_id)
        return TicketSerializer(tickets, many=True).data

class SeatService:
    @staticmethod
    def create_seat(data):
        """Tạo ghế mới"""
        serializer = SeatSerializer(data=data)
        if serializer.is_valid():
            seat = serializer.save()
            return seat
        return None

    @staticmethod
    def get_seats_by_room(room_id):
        """Lấy danh sách ghế theo phòng chiếu"""
        seats = Seat.objects.filter(room_id=room_id)
        return SeatSerializer(seats, many=True).data

    @staticmethod
    def get_available_seats(showtime_id):
        """Lấy danh sách ghế còn trống theo suất chiếu"""
        booked_seats = Booking.objects.filter(
            showtime_id=showtime_id
        ).values_list('seats', flat=True)
        available_seats = Seat.objects.exclude(id__in=booked_seats)
        return SeatSerializer(available_seats, many=True).data 