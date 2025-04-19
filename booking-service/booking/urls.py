from django.urls import path
from . import views

urlpatterns = [
    # API đặt vé
    path('bookings/', views.BookingViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='booking-list'),
    
    path('bookings/<int:pk>/', views.BookingViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='booking-detail'),
    
    path('bookings/<int:pk>/cancel/', views.BookingViewSet.as_view({
        'post': 'cancel'
    }), name='booking-cancel'),
    
    path('bookings/user/<int:user_id>/', views.BookingViewSet.as_view({
        'get': 'by_user'
    }), name='booking-by-user'),
    
    path('bookings/showtime/<int:showtime_id>/', views.BookingViewSet.as_view({
        'get': 'by_showtime'
    }), name='booking-by-showtime'),
    
    path('bookings/check-seat/', views.BookingViewSet.as_view({
        'post': 'check_seat'
    }), name='booking-check-seat'),
    
    path('bookings/calculate-price/', views.BookingViewSet.as_view({
        'post': 'calculate_price'
    }), name='booking-calculate-price'),
    
    path('bookings/payment/', views.BookingViewSet.as_view({
        'post': 'process_payment'
    }), name='booking-payment'),
    
    # API vé
    path('tickets/', views.TicketViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='ticket-list'),
    
    path('tickets/<int:pk>/', views.TicketViewSet.as_view({
        'get': 'retrieve'
    }), name='ticket-detail'),
    
    path('tickets/booking/<int:booking_id>/', views.TicketViewSet.as_view({
        'get': 'by_booking'
    }), name='ticket-by-booking'),
    
    # API ghế
    path('seats/', views.SeatViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='seat-list'),
    
    path('seats/<int:pk>/', views.SeatViewSet.as_view({
        'get': 'retrieve'
    }), name='seat-detail'),
    
    path('seats/room/<int:room_id>/', views.SeatViewSet.as_view({
        'get': 'by_room'
    }), name='seat-by-room'),
    
    path('seats/available/', views.SeatViewSet.as_view({
        'get': 'available'
    }), name='seat-available'),
] 