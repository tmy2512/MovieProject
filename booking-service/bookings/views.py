from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import (
    Booking, Seat, DiscountCode, Combo, ComboItem,
    Voucher, GroupBooking, GroupBookingMember
)
from .serializers import (
    BookingSerializer, BookingCreateSerializer,
    DiscountCodeSerializer, ComboSerializer,
    VoucherSerializer, GroupBookingSerializer,
    GroupBookingMemberSerializer
)

class DiscountCodeViewSet(viewsets.ModelViewSet):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer

    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        try:
            discount_code = DiscountCode.objects.get(code=code)
            if discount_code.is_valid():
                return Response({
                    'valid': True,
                    'discount_percent': discount_code.discount_percent
                })
            return Response({
                'valid': False,
                'message': 'Mã giảm giá không hợp lệ hoặc đã hết hạn'
            })
        except DiscountCode.DoesNotExist:
            return Response({
                'valid': False,
                'message': 'Mã giảm giá không tồn tại'
            })

class ComboViewSet(viewsets.ModelViewSet):
    queryset = Combo.objects.filter(is_active=True)
    serializer_class = ComboSerializer

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

    @action(detail=False, methods=['post'])
    def validate(self, request):
        code = request.data.get('code')
        try:
            voucher = Voucher.objects.get(code=code)
            if voucher.is_valid():
                return Response({
                    'valid': True,
                    'value': voucher.value
                })
            return Response({
                'valid': False,
                'message': 'Voucher không hợp lệ hoặc đã hết hạn'
            })
        except Voucher.DoesNotExist:
            return Response({
                'valid': False,
                'message': 'Voucher không tồn tại'
            })

class GroupBookingViewSet(viewsets.ModelViewSet):
    queryset = GroupBooking.objects.all()
    serializer_class = GroupBookingSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        group_booking = self.get_object()
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')
        
        member = GroupBookingMember.objects.create(
            group_booking=group_booking,
            user_id=user_id,
            amount=amount
        )
        
        return Response(GroupBookingMemberSerializer(member).data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        group_booking = self.get_object()
        group_booking.status = 'confirmed'
        group_booking.save()
        
        # Cập nhật trạng thái cho tất cả thành viên
        GroupBookingMember.objects.filter(
            group_booking=group_booking
        ).update(status='paid')
        
        return Response(GroupBookingSerializer(group_booking).data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Xử lý mã giảm giá
        discount_code = None
        if 'discount_code' in serializer.validated_data:
            try:
                discount_code = DiscountCode.objects.get(
                    code=serializer.validated_data['discount_code']
                )
                if not discount_code.is_valid():
                    return Response({
                        'error': 'Mã giảm giá không hợp lệ hoặc đã hết hạn'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except DiscountCode.DoesNotExist:
                return Response({
                    'error': 'Mã giảm giá không tồn tại'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý voucher
        voucher = None
        if 'voucher' in serializer.validated_data:
            try:
                voucher = Voucher.objects.get(
                    code=serializer.validated_data['voucher']
                )
                if not voucher.is_valid():
                    return Response({
                        'error': 'Voucher không hợp lệ hoặc đã hết hạn'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Voucher.DoesNotExist:
                return Response({
                    'error': 'Voucher không tồn tại'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Xử lý combo
        combo = None
        if 'combo' in serializer.validated_data:
            try:
                combo = Combo.objects.get(
                    id=serializer.validated_data['combo']
                )
                if not combo.is_active:
                    return Response({
                        'error': 'Combo không còn hoạt động'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Combo.DoesNotExist:
                return Response({
                    'error': 'Combo không tồn tại'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Tạo booking
        booking = serializer.save(
            discount_code=discount_code,
            voucher=voucher,
            combo=combo
        )

        # Nếu là đặt vé nhóm
        if serializer.validated_data.get('is_group_booking'):
            group_booking = GroupBooking.objects.create(
                booking=booking,
                group_leader=booking.user,
                total_amount=booking.total_amount
            )

        return Response(BookingSerializer(booking).data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        booking = self.get_object()
        return Response(booking.booking_history)

    @action(detail=True, methods=['post'])
    def apply_discount(self, request, pk=None):
        booking = self.get_object()
        code = request.data.get('code')
        
        try:
            discount_code = DiscountCode.objects.get(code=code)
            if not discount_code.is_valid():
                return Response({
                    'error': 'Mã giảm giá không hợp lệ hoặc đã hết hạn'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Áp dụng giảm giá
            discount_amount = booking.total_amount * discount_code.discount_percent / 100
            booking.total_amount -= discount_amount
            booking.discount_code = discount_code
            booking.save()
            
            # Cập nhật lịch sử
            booking.booking_history['price_changes'].append({
                'type': 'discount',
                'amount': discount_amount,
                'timestamp': timezone.now().isoformat()
            })
            booking.save()
            
            return Response(BookingSerializer(booking).data)
        except DiscountCode.DoesNotExist:
            return Response({
                'error': 'Mã giảm giá không tồn tại'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def apply_voucher(self, request, pk=None):
        booking = self.get_object()
        code = request.data.get('code')
        
        try:
            voucher = Voucher.objects.get(code=code)
            if not voucher.is_valid():
                return Response({
                    'error': 'Voucher không hợp lệ hoặc đã hết hạn'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Áp dụng voucher
            booking.total_amount -= voucher.value
            booking.voucher = voucher
            booking.save()
            
            # Cập nhật lịch sử
            booking.booking_history['price_changes'].append({
                'type': 'voucher',
                'amount': voucher.value,
                'timestamp': timezone.now().isoformat()
            })
            booking.save()
            
            return Response(BookingSerializer(booking).data)
        except Voucher.DoesNotExist:
            return Response({
                'error': 'Voucher không tồn tại'
            }, status=status.HTTP_400_BAD_REQUEST) 