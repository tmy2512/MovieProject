from django.urls import path
from . import views

urlpatterns = [
    # API phim
    path('movies/', views.MovieViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='movie-list'),
    
    path('movies/<int:pk>/', views.MovieViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='movie-detail'),
    
    path('movies/search/', views.MovieViewSet.as_view({
        'get': 'search'
    }), name='movie-search'),
    
    path('movies/filter/', views.MovieViewSet.as_view({
        'get': 'filter'
    }), name='movie-filter'),
    
    path('movies/upcoming/', views.MovieViewSet.as_view({
        'get': 'upcoming'
    }), name='movie-upcoming'),
    
    path('movies/now-showing/', views.MovieViewSet.as_view({
        'get': 'now_showing'
    }), name='movie-now-showing'),
    
    # API thể loại
    path('genres/', views.GenreViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='genre-list'),
    
    path('genres/<int:pk>/', views.GenreViewSet.as_view({
        'get': 'retrieve'
    }), name='genre-detail'),
    
    path('genres/<int:pk>/movies/', views.GenreViewSet.as_view({
        'get': 'movies'
    }), name='genre-movies'),
    
    # API diễn viên
    path('actors/', views.ActorViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='actor-list'),
    
    path('actors/<int:pk>/', views.ActorViewSet.as_view({
        'get': 'retrieve'
    }), name='actor-detail'),
    
    path('actors/<int:pk>/movies/', views.ActorViewSet.as_view({
        'get': 'movies'
    }), name='actor-movies'),
] 