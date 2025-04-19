from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'genre', 'director')
    list_filter = ('genre', 'release_date', 'rating')
    search_fields = ('title', 'description', 'director', 'cast')
    date_hierarchy = 'release_date'
    ordering = ('-release_date',)
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'description', 'poster_url')
        }),
        ('Chi tiết phim', {
            'fields': ('duration', 'release_date', 'rating', 'genre')
        }),
        ('Đội ngũ sản xuất', {
            'fields': ('director', 'cast')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at') 