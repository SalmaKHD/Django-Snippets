from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from accounts.forms import RegistrationForm, LoginForm


# Create your views here.

def register(request):
    form = UserCreationForm(request.POST) # default form
    form = RegistrationForm(request.POST) # custom form
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('movies:thank_you'))
    return render(request, 'accounts/register.html', {'form': form})

def auth_login(request):
    if request.user.is_authenticated: # user field added by middleware
        return HttpResponseRedirect(reverse('movies:thank-you'))
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST) # default form
        form = LoginForm(request=request, data=request.POST) # custom login form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # User if valid else None
            if user is not None:
                login(request, user)
                return HttpResponse(f"Successfully logged in {user}")
    form = LoginForm()
    return render(request, 'accounts/register.html', {'form': form})

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('movies:template'))
