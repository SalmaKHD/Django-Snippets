from django.db import models
from django.utils import timezone


# Create your models here.
class Genre(models.Model):  # all functionalities for storing data in db are already available in models.Model class
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name  # to change representation of obj in panel (when adding a record for example)


# any class inheriting from the Model class represents a table in db
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    number_in_stock = models.IntegerField()
    daily_rent = models.FloatField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
