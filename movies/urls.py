from django.urls import path

from . import views

# no need for specifying a prefix for each path
app_name = 'movies' # for not having to prefix url names with app name to avoid calling urls inadvertently within other apps

# define url config
urlpatterns = [
    path('', views.index, name='index'), # represents the root of urls that this path object will handle
    path('template', views.template, name='template'),
    # a path that is an int
    path('<int:movie_id>', views.detail, name='detail'), # names useful when changing path names later on
    path('details/<int:movie_id>', views.details, name='details'),
    path('purchase', views.purchase, name='purchase'),
    path('new/<str:title>/<int:release_year>/<int:number_in_stock>/<int:daily_rent>/<str:genre>/<str:description>', views.new, name="new"),
    path('movie_form', views.movie_form),
    path('thank_you', views.thank_you),
    path('update/<int:movie_id>', views.update_movie),
    path('cookie', views.cookie)
]