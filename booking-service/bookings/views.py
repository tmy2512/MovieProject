from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 