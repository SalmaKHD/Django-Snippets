from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.aggregates import Max, Min
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, UpdateView, \
    DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .tasks import send_movie_added_email
from .forms import MoviesForm, MovieFormModel
from .models import Movie, Genre
from rest_framework import viewsets, permissions
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import MovieSerializer


# Create your views here.

def index(request):
    movies = Movie.objects.all()  # SELECT # FROM movie
    Movie.objects.filter(release_year=1984)  # SELECT * FROM movie WHERE release_year=1984, keyword args
    Movie.objects.get(id=1)
    output = ', '.join([movie.title for movie in movies])
    return HttpResponse(movies)

def cookie(request):
    # set cookie
    # set a cookie, alive for current session only
    response = HttpResponse("Set")
    response.set_cookie('theme', 'dark', max_age=5, httponly=True, secure=True) # won't set cookies otherwise
    response.set_cookie('name', 'Rahul')
    # get cookie
    print(request.COOKIES['name'])
    response.delete_cookie('name')
    # print(request.COOKIES['name'])
    return HttpResponse('Cookie Operations Done!')

def session(request):
    request.session['id'] = 20
    session_id = request.session['id']
    # delete entire session
    # request.session.flush()
    request.session.set_expiry(20) # default is 2 weeks
    request.session.clear_expired()
    request.session['dict'] = {'name': 'Titanic'}
    request.session['dict']['name'] = 'The Office'
    # we have to save changes in this case
    request.session.modifier = True
    print(f'Name of movie is: {request.session['dict']['name']}')
    return HttpResponse(f"Session started. Session id is: {session_id}")

def template(request):
    query = request.GET.get('query', None)
    per_page_item_number = 4
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('id')
        paginator = Paginator(movies, per_page_item_number)
    else:
        # returns a query set, all lazy: not executed until accessed
        movies = Movie.objects.all().order_by('id')
        paginator = Paginator(movies, per_page_item_number, orphans=0, allow_empty_first_page=True)

    page_number = request.GET.get('p', 1) # access p parameter in request
    movies_result = paginator.get_page(page_number) # it will return the last page if nothing exists
    # queryset methods (for querying the database)
    return render(request, 'movies/template.html', {'movies': movies_result, 'query': query})

def example_queries():
    # *** example db operations ***
    movies = Movie.objects.all().order_by('id')
    # get object by id
    print(movies.get(id=4))  # will raise an exception if more than 1 obj or no obj
    # get objects matching a condition
    print(Movie.objects.filter(title="Titanic"))
    # get objects not matching a condition
    print(Movie.objects.exclude(title="The Office"))  # returns a query set
    # get access to first object (works like a list)
    print(movies[0])  # returns an object
    # get objects by order
    print(Movie.objects.order_by('title'))
    print(Movie.objects.order_by('-title'))  # for reverse order
    print(Movie.objects.order_by('title').reverse())
    # get objects as a dictionary list
    print(Movie.objects.values())
    # get row count
    print(Movie.objects.count())
    # get first object
    print(Movie.objects.first())
    print(Movie.objects.last())
    titanic = Movie.objects.get(title="The Office")  # throws an exception if it does not exist
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
    print(Movie.objects.filter(title__gt='T'))  # field look up
    print(Movie.objects.filter(title__istartswith='T'))  # field look up
    print(Movie.objects.filter(id__in=[1, 2]))  # field look up
    # update a row in table
    movie = Movie.objects.get(pk=4)
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
    # *** example db operations end ***

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

def new_movie(request):
    if request.method == 'POST':
        form = MovieFormModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/movies/template')
    else:
        form = MovieFormModel()
    return render(request, 'movies/basic_form.html', {'form': form})


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

def hook_template(request):
    return TemplateResponse(request, 'movies/hook_template.html', {"name": "The Office"})

def get_movies_with_genre(request, genre):
    movies = Movie.objects.filter(genre__name = genre)
    # or
    # genre = Genre.objects.get(name=genre)
    # movies = genre.movies.all() # movies_set is a model manager like objects
    result = "No movies found"
    if movies:
        print(movies.first().genre)
        result = movies
    return HttpResponse(result)

# class-based views
class MovieView(View):
    def get(self, request):
        form = MovieFormModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/movies/template')
        return HttpResponse("invalid form")

    def post(self, request):
        form = MovieFormModel()
        return render(request, 'movies/basic_form.html', {'form': form})

class AboutView(TemplateView):
    template_name ="movies/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_name'] = "Something"
        return context

class RedirectAbout(RedirectView):
    url = '/movies/about'
    pattern_name = "about"
    query_string = True # to pass query params also

class MoviesView(ListView):
    model = Movie
    template_name = "movies/movies.html"

class MovieDetailView(DetailView):
    model = Movie

class MovieFormView(FormView):
    template_name = "movies/form.html"
    form_class = MoviesForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class AddMovieView(CreateView):
    form_class = MoviesForm
    template_name = "movies/form.html"

class UpdateMovieView(UpdateView):
    model = Movie
    form_class = MoviesForm
    template_name = "movies/form.html"

class DeleteMovieView(DeleteView):
    model = Movie

# Django DRF
# viewsets.ModelViewSet -> has everything we need -> all CRUD operations supported
class MovieViewSet(viewsets.ModelViewSet):
    queryset = (Movie.objects.all() # which data to work with
                .prefetch_related('tags') # optimization, for single joins rather than on each object
                .select_related('genre')) # optimization, for single joins rather than on each object
    serializer_class = MovieSerializer # specifies serializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genre__name']
    search_fields = ['title', 'genre__name']  # genre is a foreign key
    ordering_fields = ['release_year']
    ordering = ['release_year'] # default order
    """
    example queries
    http://127.0.0.1:8000/movies/movies-drf/?page=3&page_size=3
    http://127.0.0.1:8000/movies/movies-drf/?genre__name=fun
    http://127.0.0.1:8000/movies/movies-drf/?search=the+office
    http://127.0.0.1:8000/movies/movies-drf/?ordering=-release_year
    """

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs) # Cache invalidated automatically on create/update/delete (DRF clears it).

    def perform_create(self, serializer):
        movie = serializer.save()
        send_movie_added_email.delay(movie.title)  # Run async

        # Send real-time notification using web sockets
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "movie_notifications",
            {
                "type": "movie_added",
                "movie": MovieSerializer(movie).data
            }
        )