from django.urls import path
from . import views

app_name = 'movies' # for not having to prefix url names with app name to avoid calling urls inadvertently within other apps

# define url config
urlpatterns = [
    path('', views.index, name='index'), # represents the root of urls that this path object will handle
    path('template', views.template, name='template'),
    # a path that is an int
    path('<int:movie_id>', views.detail, name='detail') # names useful when changing path names later on
]