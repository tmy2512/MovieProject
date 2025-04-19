from rest_framework import serializers
from .models import Payment, Refund
from .gateways import VNPayGateway

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'
        read_only_fields = ('status', 'transaction_id')

class PaymentSerializer(serializers.ModelSerializer):
    refunds = RefundSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('status', 'transaction_id', 'payment_url')

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['booking_id', 'user_id', 'amount', 'payment_method']

    def create(self, validated_data):
        # Tạo payment record
        payment = Payment.objects.create(**validated_data)

        # Nếu là thanh toán qua VNPay, tạo URL thanh toán
        if payment.payment_method == 'VNPAY':
            try:
                gateway = VNPayGateway()
                payment_info = gateway.create_payment(
                    amount=float(payment.amount),
                    order_info=f"Thanh toán vé xem phim - Booking {payment.booking_id}"
                )
                payment.payment_url = payment_info['payment_url']
                payment.transaction_id = payment_info['transaction_id']
                payment.save()
            except Exception as e:
                payment.status = 'FAILED'
                payment.save()
                raise serializers.ValidationError(str(e))

        return payment

class RefundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['payment', 'amount', 'reason']

    def create(self, validated_data):
        payment = validated_data['payment']
        
        # Kiểm tra xem payment có thể hoàn tiền không
        if payment.status != 'COMPLETED':
            raise serializers.ValidationError("Chỉ có thể hoàn tiền cho các giao dịch đã hoàn tất")
            
        if payment.status == 'REFUNDED':
            raise serializers.ValidationError("Giao dịch này đã được hoàn tiền")

        # Tạo refund record
        refund = Refund.objects.create(**validated_data)

        # Xử lý hoàn tiền qua payment gateway
        if payment.payment_method == 'VNPAY':
            try:
                gateway = VNPayGateway()
                refund_info = gateway.process_refund(
                    transaction_id=payment.transaction_id,
                    amount=float(refund.amount),
                    reason=refund.reason
                )
                
                if 'error' in refund_info:
                    refund.status = 'FAILED'
                    refund.save()
                    raise serializers.ValidationError(refund_info['error'])
                    
                refund.transaction_id = refund_info.get('transaction_id')
                refund.status = 'COMPLETED'
                refund.save()
                
                # Cập nhật trạng thái payment
                payment.status = 'REFUNDED'
                payment.save()
                
            except Exception as e:
                refund.status = 'FAILED'
                refund.save()
                raise serializers.ValidationError(str(e))

        return refund 