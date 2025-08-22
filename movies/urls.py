from django.urls import path
from . import views

# define url config
urlpatterns = [
    path('', views.index, name='movies_index'), # represents the root of urls that this path object will handle
    path('template', views.template, name='movies_template'),
    # a path that is an int
    path('<int:movie_id>', views.detail, name='movies_detail') # names useful when changing path names later on
]