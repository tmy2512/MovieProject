from django.db import models
from decimal import Decimal

class Payment(models.Model):
    booking_id = models.IntegerField()
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('VNPAY', 'VNPay'),
            ('MOMO', 'MoMo'),
            ('CASH', 'Tiền mặt'),
        ],
        default='VNPAY'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Chờ thanh toán'),
            ('PROCESSING', 'Đang xử lý'),
            ('COMPLETED', 'Đã thanh toán'),
            ('FAILED', 'Thất bại'),
            ('REFUNDED', 'Đã hoàn tiền'),
        ],
        default='PENDING'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['booking_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f"Payment {self.id} - Booking {self.booking_id} - {self.amount} VND"

class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Chờ xử lý'),
            ('PROCESSING', 'Đang xử lý'),
            ('COMPLETED', 'Đã hoàn tiền'),
            ('FAILED', 'Thất bại'),
        ],
        default='PENDING'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Refund {self.id} - Payment {self.payment_id} - {self.amount} VND"

    def save(self, *args, **kwargs):
        if not self.amount:
            self.amount = self.payment.amount
        super().save(*args, **kwargs) 