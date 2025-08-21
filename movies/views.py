from django.http import HttpResponse
from django.shortcuts import render

from .models import Movie

# Create your views here.

def index(request):
    movies = Movie. objects.all() # SELECT # FROM movie
    Movie.objects.filter(release_year=1984) # SELECT * FROM movie WHERE release_year=1984, keyword args
    Movie.objects.get(id = 1)
    output = ', '.join([[movie.title for movie in movies]])
    return HttpResponse(movies)

def template(request):
    movies = Movie.objects.all()
    return render(request, 'movies/template.html', {'movies': movies})