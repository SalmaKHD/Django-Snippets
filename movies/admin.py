from django.contrib import admin
from .models import Genre, Movie

# for customizing admin panel
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    exclude = ('date_created', )
    list_display = ('id', 'title', 'number_in_stock', 'daily_rent') # customizes column display for records in this table
    list_display_links = ['title'] # makes it a link to obj also
    list_filter = ['date_created']
    search_fields = ['title']

# Register your models here.
admin.site.register(Genre, GenreAdmin)
# admin.site.register(Movie, MovieAdmin)
