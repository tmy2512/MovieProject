from rest_framework import serializers
import requests
from django.conf import settings
from .models import (
    Booking, Seat, DiscountCode, Combo, ComboItem,
    Voucher, GroupBooking, GroupBookingMember
)

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
        read_only_fields = ('current_uses', 'created_at', 'updated_at')

class ComboItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboItem
        fields = '__all__'

class ComboSerializer(serializers.ModelSerializer):
    items = ComboItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Combo
        fields = '__all__'

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'
        read_only_fields = ('current_uses', 'created_at', 'updated_at')

class GroupBookingMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBookingMember
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class GroupBookingSerializer(serializers.ModelSerializer):
    members = GroupBookingMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = GroupBooking
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    discount_code = DiscountCodeSerializer(read_only=True)
    voucher = VoucherSerializer(read_only=True)
    combo = ComboSerializer(read_only=True)
    group_bookings = GroupBookingSerializer(many=True, read_only=True)
    movie_details = serializers.SerializerMethodField()
    showtime_details = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_movie_details(self, obj):
        try:
            # Lấy thông tin showtime trước
            showtime_response = requests.get(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/{obj.showtime_id}/"
            )
            if showtime_response.status_code == 200:
                showtime_data = showtime_response.json()
                movie_id = showtime_data.get('movie_id')
                
                # Sau đó lấy thông tin phim
                movie_response = requests.get(
                    f"{settings.MOVIE_SERVICE_URL}/api/movies/{movie_id}/"
                )
                if movie_response.status_code == 200:
                    return movie_response.json()
            return None
        except requests.RequestException:
            return None

    def get_showtime_details(self, obj):
        try:
            response = requests.get(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/{obj.showtime_id}/"
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

class BookingCreateSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, required=True)
    discount_code = serializers.CharField(required=False, allow_null=True)
    voucher = serializers.CharField(required=False, allow_null=True)
    combo = serializers.IntegerField(required=False, allow_null=True)
    is_group_booking = serializers.BooleanField(default=False)

    class Meta:
        model = Booking
        fields = [
            'user_id', 'showtime_id', 'number_of_seats', 'seats',
            'total_amount', 'status', 'discount_code', 'voucher', 'combo',
            'is_group_booking'
        ]

    def validate(self, data):
        # Kiểm tra số lượng ghế
        if len(data['seats']) != data['number_of_seats']:
            raise serializers.ValidationError(
                "Số lượng ghế không khớp với số lượng đã chọn"
            )

        # Kiểm tra tính hợp lệ của showtime
        try:
            response = requests.get(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/{data['showtime_id']}/"
            )
            if response.status_code != 200:
                raise serializers.ValidationError("Suất chiếu không tồn tại")
                
            showtime_data = response.json()
            if showtime_data['status'] != 'OPEN':
                raise serializers.ValidationError("Suất chiếu này không còn mở đặt vé")
                
            if showtime_data['available_seats'] < data['number_of_seats']:
                raise serializers.ValidationError("Không đủ ghế trống cho đặt vé này")
                
            # Tính tổng giá vé
            data['total_amount'] = showtime_data['price'] * data['number_of_seats']
            
        except requests.RequestException:
            raise serializers.ValidationError("Không thể kết nối đến showtime service")

        return data

    def create(self, validated_data):
        seats_data = validated_data.pop('seats')
        booking = Booking.objects.create(**validated_data)
        
        for seat_data in seats_data:
            Seat.objects.create(booking=booking, **seat_data)
            
        return booking 