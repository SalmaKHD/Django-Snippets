from django import forms
from django.db.models.fields import CharField


class MoviesForm(forms.Form):
    title = forms.CharField(min_length=5, label_suffix='')
    release_year = forms.IntegerField(label='Release Year',
                                      label_suffix='',
                                      # min_value=1880,
                                      error_messages={'min_value': 'min release year must be 1880'}
                                      )
    number_in_stock = forms.IntegerField(label='Number in Stock', label_suffix='')
    daily_rent = forms.FloatField(label='Daily Rent', label_suffix='')
    description = forms.CharField(label='Description', label_suffix='', widget=forms.Textarea(attrs={'cols':5})) # targets html code generated for the form