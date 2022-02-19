from django.urls        import path

from .views import MovieListAPIView, MovieDetailAPIView


urlpatterns = [
    path('list/', MovieListAPIView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
]