from django.contrib.auth.models import User
from django.test import TestCase
from openpyexcel.styles.builtins import title
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from movies.models import Movie, Genre


# Create your tests here.
class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="something")
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'password123')
        self.user = User.objects.create_user('user', 'user@gmail.com', 'password212')
        self.movie =  Movie.objects.create(
        title="Something", release_year=1991, number_in_stock=12, daily_rent=45.0,
        genre=self.genre, description="some movie"
    )
        self.list_url = reverse('movies:movies-drf-list')

    def test_list_movies_unuthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_movie_as_admin(self):
        self.client.login(username='admin', password='password123')
        self.genre = Genre.objects.create(name="something")
        data = {
            "title": "New Movie",
            "year": 2024,
            "number_in_stock": 5,
            "genre": self.genre
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

    def test_create_movie_as_regular_user(self):
        self.client.login(username='user', password='password212')
        self.genre = Genre.objects.create(name="something")
        data = {"title": "Forbidden Movie", "year": 2025, "number_in_stock": 1, "genre": self.genre}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)