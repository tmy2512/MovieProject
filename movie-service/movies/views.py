from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie
from .serializers import MovieSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'genre', 'language']
    search_fields = ['title', 'description', 'director', 'cast']
    ordering_fields = ['release_date', 'rating']

    @action(detail=False, methods=['get'])
    def now_showing(self, request):
        movies = Movie.objects.filter(status='NOW_SHOWING')
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def coming_soon(self, request):
        movies = Movie.objects.filter(status='COMING_SOON')
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data) 