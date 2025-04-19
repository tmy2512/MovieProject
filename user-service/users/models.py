from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Thêm trường để lưu điểm thưởng của khách hàng
    loyalty_points = models.IntegerField(default=0)
    
    # Cấp độ thành viên
    MEMBERSHIP_CHOICES = [
        ('BRONZE', 'Bronze'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
    ]
    membership_level = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_CHOICES,
        default='BRONZE'
    )

    class Meta:
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['membership_level']),
        ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def update_membership_level(self):
        """Cập nhật cấp độ thành viên dựa trên điểm thưởng"""
        if self.loyalty_points >= 10000:
            self.membership_level = 'PLATINUM'
        elif self.loyalty_points >= 5000:
            self.membership_level = 'GOLD'
        elif self.loyalty_points >= 2000:
            self.membership_level = 'SILVER'
        else:
            self.membership_level = 'BRONZE'
        self.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorite_genres = models.JSONField(default=list)  # Thể loại phim yêu thích
    preferred_theaters = models.JSONField(default=list)  # Rạp ưa thích
    notification_preferences = models.JSONField(default=dict)  # Cài đặt thông báo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}" 