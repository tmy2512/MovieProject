from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TheaterViewSet, ShowtimeViewSet

router = DefaultRouter()
router.register(r'theaters', TheaterViewSet)
router.register(r'showtimes', ShowtimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 