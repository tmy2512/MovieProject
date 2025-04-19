from django.db import models
from django.utils import timezone

class RevenueReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tickets = models.IntegerField(default=0)
    total_showtimes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Báo cáo từ {self.start_date} đến {self.end_date}"

class MovieRevenue(models.Model):
    report = models.ForeignKey(RevenueReport, on_delete=models.CASCADE, related_name='movie_revenues')
    movie_id = models.IntegerField()
    movie_title = models.CharField(max_length=255)
    ticket_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-revenue']

    def __str__(self):
        return f"{self.movie_title} - {self.revenue}"

class DailyRevenue(models.Model):
    report = models.ForeignKey(RevenueReport, on_delete=models.CASCADE, related_name='daily_revenues')
    date = models.DateField()
    ticket_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.revenue}"

class TheaterRevenue(models.Model):
    report = models.ForeignKey(RevenueReport, on_delete=models.CASCADE, related_name='theater_revenues')
    theater_id = models.IntegerField()
    theater_name = models.CharField(max_length=255)
    ticket_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-revenue']

    def __str__(self):
        return f"{self.theater_name} - {self.revenue}"

class ShowtimeRevenue(models.Model):
    report = models.ForeignKey(RevenueReport, on_delete=models.CASCADE, related_name='showtime_revenues')
    showtime_id = models.IntegerField()
    movie_title = models.CharField(max_length=255)
    theater_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    ticket_count = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-revenue']

    def __str__(self):
        return f"{self.movie_title} - {self.start_time} - {self.revenue}" 