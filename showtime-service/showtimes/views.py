from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .models import Theater, Showtime
from .serializers import TheaterSerializer, ShowtimeSerializer, ShowtimeCreateSerializer

class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'screen_type']

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movie_id', 'theater', 'status']
    search_fields = ['movie_id', 'theater__name']
    ordering_fields = ['start_time', 'price']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ShowtimeCreateSerializer
        return ShowtimeSerializer

    @action(detail=False, methods=['get'])
    def by_movie(self, request):
        movie_id = request.query_params.get('movie_id')
        date = request.query_params.get('date')
        
        if not movie_id:
            return Response({"error": "movie_id is required"}, status=400)
            
        queryset = self.queryset.filter(movie_id=movie_id, status='OPEN')
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                queryset = queryset.filter(
                    start_time__year=date_obj.year,
                    start_time__month=date_obj.month,
                    start_time__day=date_obj.day
                )
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
                
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_theater(self, request):
        theater_id = request.query_params.get('theater_id')
        date = request.query_params.get('date')
        
        if not theater_id:
            return Response({"error": "theater_id is required"}, status=400)
            
        queryset = self.queryset.filter(theater_id=theater_id, status='OPEN')
        
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                queryset = queryset.filter(
                    start_time__year=date_obj.year,
                    start_time__month=date_obj.month,
                    start_time__day=date_obj.day
                )
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
                
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 