from django.db.models import Q
from django.db.models.aggregates import Max, Min
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import MoviesForm, MovieFormModel
from .models import Movie, Genre


# Create your views here.

def index(request):
    movies = Movie.objects.all()  # SELECT # FROM movie
    Movie.objects.filter(release_year=1984)  # SELECT * FROM movie WHERE release_year=1984, keyword args
    Movie.objects.get(id=1)
    output = ', '.join([movie.title for movie in movies])
    return HttpResponse(movies)


def template(request):
    # returns a query set, all lazy: not executed until accessed
    movies = Movie.objects.all()
    # queryset methods (for querying the database)
    # get object by id
    print(movies.get(id=1))  # will raise an exception if more than 1 obj or no obj
    # get objects matching a condition
    print(Movie.objects.filter(title="Titanic"))
    # get objects not matching a condition
    print(Movie.objects.exclude(title="The Office")) # returns a query set
    # get access to first object (works like a list)
    print(movies[0]) # returns an object
    # get objects by order
    print(Movie.objects.order_by('title'))
    print(Movie.objects.order_by('-title')) # for reverse order
    print(Movie.objects.order_by('title').reverse())
    # get objects as a dictionary list
    print(Movie.objects.values())
    # get row count
    print(Movie.objects.count())
    # get first object
    print(Movie.objects.first())
    print(Movie.objects.last())
    titanic = Movie.objects.get(title="The Office") # throws an exception if it does not exist
    print(Movie.objects.contains(titanic))
    # compound conditions
    print(movies.filter(title="Titanic") & movies.filter(release_year=1876))
    print(movies.filter(title="Titanic") | movies.filter(title="The Office"))
    # use Q object to query the database
    print(movies.filter(Q(title="Titanic") | ~Q(title="The Office")))
    # slicing
    print(movies[1:2])
    # field look-up queries
    # field lookups: Model.objects.filter(field__lookup=)
    print(Movie.objects.filter(title__gt='T')) # field look up
    print(Movie.objects.filter(title__istartswith='T')) # field look up
    print(Movie.objects.filter(id__in=[1,2])) # field look up
    # update a row in table
    movie = Movie.objects.get(pk=1)
    movie.title = "Titanicc"
    movie.save()
    # update multiple rows
    Movie.objects.filter(title__startswith="The").update(release_year=1954)
    print(Movie.objects.get(id=4).release_year)
    # delete an object or objects
    Movie.objects.create(
        title="Something", release_year=1991, number_in_stock=12, daily_rent=45.0,
        genre=Genre.objects.get(pk=1), description="some movie"
    )
    Movie.objects.filter(title="Something").delete()
    # aggregation in Django
    print(Movie.objects.all().aggregate(max=Max('daily_rent'), min=Min('daily_rent')))
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

def movie_form(request):
    form = MoviesForm(request.POST) # store data in form    form = MovieFormModel(request.POST)
    if form.is_valid(): # if form is valid, continue
        print(form.cleaned_data)
        # save movie to database
        Movie.objects.create(
            title=form.cleaned_data['title'],
            release_year=form.cleaned_data['release_year'],
            number_in_stock=form.cleaned_data['number_in_stock'],
            daily_rent=form.cleaned_data['daily_rent'],
            genre = Genre.objects.get(pk=1),
            description=form.cleaned_data['description']
        )
        # form.save()
        return HttpResponseRedirect('thank_you')
    return render(request, 'movies/form.html', {'form': form}) # return form again if invalid

def thank_you(request):
    return HttpResponse("Thank you for submitting!")

def update_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'POST':
        form = MoviesForm(request.POST)
        if form.is_valid():
            movie.title = form.cleaned_data['title']
            movie.release_year = form.cleaned_data['release_year']
            movie.number_in_stock = form.cleaned_data['number_in_stock']
            movie.daily_rent = form.cleaned_data['daily_rent']
            movie.description = form.cleaned_data['description']
            movie.save()
            print(movie.description)
            return HttpResponse("Form saved successfully")

    form = MoviesForm(initial={'title':movie.title,
                                   'release_year':movie.release_year,
                                   'number_in_stock':movie.number_in_stock,
                                   'daily_rent': movie.daily_rent,
                                   'description': movie.description
                                   }
                          )
    return render(request, 'movies/form.html', {'form': form})