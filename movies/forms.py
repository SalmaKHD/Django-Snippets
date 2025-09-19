from django import forms
from django.core import validators

from movies.models import Movie


def starts_with_capital(value):
    return value[0].isupper()

class MoviesForm(forms.Form):
    title = forms.CharField(min_length=5, label_suffix='', validators=[validators.MinLengthValidator(5),starts_with_capital])
    release_year = forms.IntegerField(label='Release Year',
                                      label_suffix='',
                                      # min_value=1880,
                                      error_messages={'min_value': 'min release year must be 1880'}
                                      )
    number_in_stock = forms.IntegerField(label='Number in Stock', label_suffix='')
    daily_rent = forms.FloatField(label='Daily Rent', label_suffix='')
    description = forms.CharField(label='Description', label_suffix='',
                                  widget=forms.Textarea(attrs={
                                      'cols':15,
                                      'placeholder': "description",
                                      'class': 'form-control'
                                  })) # targets html code generated for the form
    def clean(self):
        super().clean()
        # title = self.cleaned_data['title']
        # if not title[0].isupper():
        #     forms.ValidationError("Title must start with an uppercase letter")


class MovieFormModel(forms.ModelForm):
    title = forms.CharField(min_length=5, label_suffix='', validators=[validators.MinLengthValidator(5),starts_with_capital])
    class Meta:
        model = Movie
        fields='__all__'
        # exclude=['genre']
        # can add the same fields here also
        labels=[],
        error_messages=[],
        help_texts=[],
        widgets=[]