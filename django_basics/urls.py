"""
URL configuration for django_basics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views
from api.models import MovieResource
from .views import home

# this is used for lookiing for paths when the user enters the url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')), # specify that direct requests that start with movies/ to urls.py file in movies app
    path('movie-api/', include(MovieResource().urls)),
    path('api/', include('movies.urls')),
    path('', views.home),
    path('accounts/', include('accounts.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Movies Admin'
admin.site.index_title = 'Movies Admin'