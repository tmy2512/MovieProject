from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'booking', 'amount', 'payment_method', 
                 'status', 'transaction_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('booking', 'amount', 'payment_method') 