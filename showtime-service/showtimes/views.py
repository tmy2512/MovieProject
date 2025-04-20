from rest_framework import viewsets, permissions
from .models import Showtime, Seat
from .serializers import ShowtimeSerializer, ShowtimeCreateSerializer, SeatSerializer

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return ShowtimeCreateSerializer
        return ShowtimeSerializer

    def get_queryset(self):
        queryset = Showtime.objects.all()
        movie_id = self.request.query_params.get('movie_id')
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)
        return queryset

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Seat.objects.all()
        showtime_id = self.request.query_params.get('showtime_id')
        if showtime_id:
            queryset = queryset.filter(showtime_id=showtime_id)
        return queryset 