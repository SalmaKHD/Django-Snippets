from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views, consumers
from .views import MoviesView, MovieFormView, MovieDetailView, AddMovieView, UpdateMovieView, DeleteMovieView, \
    MovieViewSet

# no need for specifying a prefix for each path
# app_name = 'movies' # for not having to prefix url names with app name to avoid calling urls inadvertently within other apps
router = DefaultRouter() # for creating endpoints automatically
router.register(r'movies-drf', MovieViewSet, basename="movie") # creates all endpoints
websocket_urlpatterns = [
    re_path(r'ws/movies/', consumers.MovieNotificationConsumer.as_view()),
]

# define url config
urlpatterns = [
    path('', views.index, name='index'), # represents the root of urls that this path object will handle
    path('cookie', views.cookie),
    path('session', views.session),
    path('template', views.template, name='template'),
    # a path that is an int
    path('<int:movie_id>', views.detail, name='detail'), # names useful when changing path names later on
    path('details/<int:movie_id>', views.details, name='details'),
    path('purchase', views.purchase, name='purchase'),
    path('new/<str:title>/<int:release_year>/<int:number_in_stock>/<int:daily_rent>/<str:genre>/<str:description>', views.new, name="new"),
    path('movie_form', views.movie_form),
    path('new', views.new_movie),
    path('thank_you', views.thank_you),
    path('update/<int:movie_id>', views.update_movie),
    path('hook-template', views.hook_template),
    path('by_genre/<str:genre>', views.get_movies_with_genre),
    path('example_queries', views.example_queries),
    path('movies-class', views.MovieView.as_view()),
    path('about', views.AboutView.as_view(), name="about"),
    path('about-redirect', views.RedirectAbout.as_view()),
    path('movies', MoviesView.as_view()),
    path('movie-details/<int:pk>', MovieDetailView.as_view()),
    path('movie-form', MovieFormView.as_view()),
    path('new-movie', AddMovieView.as_view()),
    path('update-movie/<int:pk>', UpdateMovieView.as_view()),
    path('delete-movie/<int:pk>', DeleteMovieView.as_view()),
    path('', include(router.urls)) # example url: http://127.0.0.1:8000/api/movies-drf/11/

]