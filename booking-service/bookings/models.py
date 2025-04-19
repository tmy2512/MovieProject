from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Booking(models.Model):
    user_id = models.IntegerField()
    showtime_id = models.IntegerField()
    number_of_seats = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed'),
        ],
        default='PENDING'
    )
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    discount_code = models.ForeignKey('DiscountCode', on_delete=models.SET_NULL, null=True, blank=True)
    voucher = models.ForeignKey('Voucher', on_delete=models.SET_NULL, null=True, blank=True)
    combo = models.ForeignKey('Combo', on_delete=models.SET_NULL, null=True, blank=True)
    is_group_booking = models.BooleanField(default=False)
    booking_history = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['showtime_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Booking {self.id} - User {self.user_id} - Showtime {self.showtime_id}"

    def save(self, *args, **kwargs):
        if not self.booking_history:
            self.booking_history = {
                'status_changes': [],
                'price_changes': [],
                'seat_changes': []
            }
        super().save(*args, **kwargs)

class Seat(models.Model):
    booking = models.ForeignKey(Booking, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=5)  # Ví dụ: A, B, C,...
    number = models.IntegerField()  # Ví dụ: 1, 2, 3,...
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('booking', 'row', 'number')
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row}{self.number}"

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_uses = models.IntegerField(default=1)
    current_uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            self.current_uses < self.max_uses
        )

    def use(self):
        if self.is_valid():
            self.current_uses += 1
            self.save()
            return True
        return False

    class Meta:
        ordering = ['-created_at']

class Combo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class ComboItem(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} x {self.quantity}"

    class Meta:
        ordering = ['-created_at']

class Voucher(models.Model):
    code = models.CharField(max_length=20, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_uses = models.IntegerField(default=1)
    current_uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            self.current_uses < self.max_uses
        )

    def use(self):
        if self.is_valid():
            self.current_uses += 1
            self.save()
            return True
        return False

    class Meta:
        ordering = ['-created_at']

class GroupBooking(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='group_bookings')
    group_leader = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='group_leader_bookings')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class GroupBookingMember(models.Model):
    group_booking = models.ForeignKey(GroupBooking, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='group_booking_memberships')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] 