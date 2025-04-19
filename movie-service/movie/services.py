from .models import Movie, Genre, Actor
from .serializers import MovieSerializer, GenreSerializer, ActorSerializer
import requests
from django.conf import settings
from datetime import datetime

class MovieService:
    @staticmethod
    def create_movie(data):
        """Tạo phim mới"""
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            movie = serializer.save()
            return movie
        return None

    @staticmethod
    def update_movie(movie_id, data):
        """Cập nhật thông tin phim"""
        try:
            movie = Movie.objects.get(id=movie_id)
            serializer = MovieSerializer(movie, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data
            return None
        except Movie.DoesNotExist:
            return None

    @staticmethod
    def delete_movie(movie_id):
        """Xóa phim"""
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
            return True
        except Movie.DoesNotExist:
            return False

    @staticmethod
    def get_movie_detail(movie_id):
        """Lấy chi tiết phim"""
        try:
            movie = Movie.objects.get(id=movie_id)
            return MovieSerializer(movie).data
        except Movie.DoesNotExist:
            return None

    @staticmethod
    def get_movies_by_genre(genre_id):
        """Lấy danh sách phim theo thể loại"""
        try:
            genre = Genre.objects.get(id=genre_id)
            movies = Movie.objects.filter(genres=genre)
            return MovieSerializer(movies, many=True).data
        except Genre.DoesNotExist:
            return None

    @staticmethod
    def get_movies_by_actor(actor_id):
        """Lấy danh sách phim theo diễn viên"""
        try:
            actor = Actor.objects.get(id=actor_id)
            movies = Movie.objects.filter(actors=actor)
            return MovieSerializer(movies, many=True).data
        except Actor.DoesNotExist:
            return None

    @staticmethod
    def search_movies(query):
        """Tìm kiếm phim"""
        movies = Movie.objects.filter(title__icontains=query)
        return MovieSerializer(movies, many=True).data

    @staticmethod
    def get_upcoming_movies():
        """Lấy danh sách phim sắp chiếu"""
        today = datetime.now().date()
        movies = Movie.objects.filter(release_date__gt=today)
        return MovieSerializer(movies, many=True).data

    @staticmethod
    def get_now_showing_movies():
        """Lấy danh sách phim đang chiếu"""
        today = datetime.now().date()
        movies = Movie.objects.filter(release_date__lte=today)
        return MovieSerializer(movies, many=True).data

class GenreService:
    @staticmethod
    def create_genre(data):
        """Tạo thể loại mới"""
        serializer = GenreSerializer(data=data)
        if serializer.is_valid():
            genre = serializer.save()
            return genre
        return None

    @staticmethod
    def get_all_genres():
        """Lấy tất cả thể loại"""
        genres = Genre.objects.all()
        return GenreSerializer(genres, many=True).data

class ActorService:
    @staticmethod
    def create_actor(data):
        """Tạo diễn viên mới"""
        serializer = ActorSerializer(data=data)
        if serializer.is_valid():
            actor = serializer.save()
            return actor
        return None

    @staticmethod
    def get_all_actors():
        """Lấy tất cả diễn viên"""
        actors = Actor.objects.all()
        return ActorSerializer(actors, many=True).data 