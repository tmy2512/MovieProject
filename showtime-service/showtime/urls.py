from django.urls import path
from . import views

urlpatterns = [
    # API suất chiếu
    path('showtimes/', views.ShowtimeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='showtime-list'),
    
    path('showtimes/<int:pk>/', views.ShowtimeViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='showtime-detail'),
    
    path('showtimes/movie/<int:movie_id>/', views.ShowtimeViewSet.as_view({
        'get': 'by_movie'
    }), name='showtime-by-movie'),
    
    path('showtimes/theater/<int:theater_id>/', views.ShowtimeViewSet.as_view({
        'get': 'by_theater'
    }), name='showtime-by-theater'),
    
    path('showtimes/date/<str:date>/', views.ShowtimeViewSet.as_view({
        'get': 'by_date'
    }), name='showtime-by-date'),
    
    path('showtimes/range/', views.ShowtimeViewSet.as_view({
        'get': 'by_date_range'
    }), name='showtime-by-range'),
    
    path('showtimes/available/', views.ShowtimeViewSet.as_view({
        'get': 'available'
    }), name='showtime-available'),
    
    # API rạp
    path('theaters/', views.TheaterViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='theater-list'),
    
    path('theaters/<int:pk>/', views.TheaterViewSet.as_view({
        'get': 'retrieve'
    }), name='theater-detail'),
    
    # API phòng chiếu
    path('rooms/', views.RoomViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='room-list'),
    
    path('rooms/<int:pk>/', views.RoomViewSet.as_view({
        'get': 'retrieve'
    }), name='room-detail'),
    
    path('rooms/theater/<int:theater_id>/', views.RoomViewSet.as_view({
        'get': 'by_theater'
    }), name='room-by-theater'),
] 