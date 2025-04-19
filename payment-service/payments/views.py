from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment, Refund
from .serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    RefundSerializer,
    RefundCreateSerializer
)
from .gateways import VNPayGateway

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['booking_id', 'user_id', 'status', 'payment_method']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        payment = self.get_object()
        
        if payment.status != 'PENDING':
            return Response(
                {"error": "Chỉ có thể xác minh giao dịch đang chờ thanh toán"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if payment.payment_method == 'VNPAY':
            try:
                gateway = VNPayGateway()
                is_valid = gateway.verify_payment(request.data)
                
                if is_valid:
                    payment.status = 'COMPLETED'
                    payment.save()
                    return Response(PaymentSerializer(payment).data)
                else:
                    payment.status = 'FAILED'
                    payment.save()
                    return Response(
                        {"error": "Xác minh thanh toán thất bại"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"error": "Phương thức thanh toán không hỗ trợ xác minh"},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        payment = self.get_object()
        
        if payment.status != 'PENDING':
            return Response(
                {"error": "Chỉ có thể hủy giao dịch đang chờ thanh toán"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = 'FAILED'
        payment.save()
        return Response(PaymentSerializer(payment).data)

class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['payment', 'status']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return RefundCreateSerializer
        return RefundSerializer 