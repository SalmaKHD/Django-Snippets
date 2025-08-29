from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from twilio.twiml.voice_response import Config

from .models import Movie, Genre


# Create your views here.

def index(request):
    movies = Movie.objects.all()  # SELECT # FROM movie
    Movie.objects.filter(release_year=1984)  # SELECT * FROM movie WHERE release_year=1984, keyword args
    Movie.objects.get(id=1)
    output = ', '.join([movie.title for movie in movies])
    return HttpResponse(movies)


def template(request):
    movies = Movie.objects.all()
    return render(request, 'movies/template.html', {'movies': movies})


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})


def purchase(request):
    # under construction
    raise Http404()  # will show default 404.html page if not in debug mode
    # return HttpResponseNotFound("Not Available")


def details(request, movie_id):
    return HttpResponseRedirect(reverse('movie_detail', args=[movie_id]))
    # return HttpResponseRedirect(f'/movies/{movie_id}')


def new(request, title, release_year, number_in_stock, daily_rent, genre, description):
    Movie.objects.create(title=title, release_year=release_year, number_in_stock=number_in_stock, daily_rent=daily_rent,
                         genre=Genre.objects.get(pk=1) if genre == "Romantic" else Genre.objects.get(pk=2), description=description)
    return HttpResponse("Insertion successful!")
