from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    director = models.CharField(max_length=255)
    cast = models.TextField()
    poster_url = models.URLField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('COMING_SOON', 'Coming Soon'),
            ('NOW_SHOWING', 'Now Showing'),
            ('ENDED', 'Ended'),
        ],
        default='COMING_SOON'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date'] 