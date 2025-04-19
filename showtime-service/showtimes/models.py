from django.db import models
from django.core.validators import MinValueValidator

class Theater(models.Model):
    name = models.CharField(max_length=255)
    seats_capacity = models.IntegerField(validators=[MinValueValidator(1)])
    screen_type = models.CharField(
        max_length=20,
        choices=[
            ('2D', '2D'),
            ('3D', '3D'),
            ('IMAX', 'IMAX'),
            ('4DX', '4DX'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.screen_type}"

class Showtime(models.Model):
    movie_id = models.IntegerField()
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('OPEN', 'Open'),
            ('FULL', 'Full'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='OPEN'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['movie_id']),
            models.Index(fields=['start_time']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Movie {self.movie_id} at {self.theater.name} - {self.start_time}" 