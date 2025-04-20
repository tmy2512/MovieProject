from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowtimeViewSet, SeatViewSet

router = DefaultRouter()
router.register(r'showtimes', ShowtimeViewSet, basename='showtime')
router.register(r'seats', SeatViewSet, basename='seat')

urlpatterns = [
    path('', include(router.urls)),
] 