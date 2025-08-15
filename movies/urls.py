from django.urls import path
from . import views

# define url config
urlpatterns = [
    path('', views.index, name='index') # represents the root of urls that this path object will handle

]