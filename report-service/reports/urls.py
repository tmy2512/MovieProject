from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RevenueReportViewSet

router = DefaultRouter()
router.register(r'reports', RevenueReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
] 