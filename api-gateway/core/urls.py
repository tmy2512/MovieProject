from django.contrib import admin
from django.urls import path, include
from gateway.views import (
    login,
    CustomTokenRefreshView,
    movie_list,
    movie_detail,
    showtime_list,
    showtime_detail,
    booking_list,
    booking_detail,
    payment_list,
    payment_detail,
    report_list,
    report_detail,
    report_export,
    report_download,
    report_summary
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/login/', login, name='login'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # Movie endpoints
    path('api/movies/', movie_list, name='movie_list'),
    path('api/movies/<int:pk>/', movie_detail, name='movie_detail'),
    
    # Showtime endpoints
    path('api/showtimes/', showtime_list, name='showtime_list'),
    path('api/showtimes/<int:pk>/', showtime_detail, name='showtime_detail'),
    
    # Booking endpoints
    path('api/bookings/', booking_list, name='booking_list'),
    path('api/bookings/<int:pk>/', booking_detail, name='booking_detail'),
    
    # Payment endpoints
    path('api/payments/', payment_list, name='payment_list'),
    path('api/payments/<int:pk>/', payment_detail, name='payment_detail'),
    
    # Report endpoints
    path('api/reports/', report_list, name='report_list'),
    path('api/reports/<int:pk>/', report_detail, name='report_detail'),
    path('api/reports/<int:pk>/export/', report_export, name='report_export'),
    path('api/reports/<int:pk>/download/', report_download, name='report_download'),
    path('api/reports/summary/', report_summary, name='report_summary'),
] 