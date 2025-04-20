from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Showtime(models.Model):
    movie_id = models.UUIDField()  # ID từ movie-service
    theater_id = models.UUIDField()  # ID từ theater-service
    screen_id = models.UUIDField()  # ID từ theater-service
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'showtimes'
        ordering = ['start_time']

    def __str__(self):
        return f"Showtime {self.id} - {self.start_time}"

    @property
    def movie(self):
        # Lấy thông tin movie từ movie-service thông qua API
        from .utils import get_movie_info
        return get_movie_info(self.movie_id)

    @property
    def theater(self):
        # Lấy thông tin theater từ theater-service thông qua API
        from .utils import get_theater_info
        return get_theater_info(self.theater_id)

    @property
    def screen(self):
        # Lấy thông tin screen từ theater-service thông qua API
        from .utils import get_screen_info
        return get_screen_info(self.screen_id)

class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=2)
    number = models.IntegerField(validators=[MinValueValidator(1)])
    is_available = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seats'
        unique_together = ['showtime', 'row', 'number']
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.row}{self.number} - {self.showtime.movie.title if self.showtime.movie else 'Unknown Movie'}" 