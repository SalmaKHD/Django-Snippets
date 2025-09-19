from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.auth_login, name='login'),
    path('logout', views.auth_logout, name='logout'),
    # path('users/', include('django.contrib.auth.urls')), # for built-in auth urls provided by Django
    path('auth-logout', LogoutView.as_view(template_name='')), # built-in logout view,
    path('auth-login', LoginView.as_view(redirect_authenticated_user=True)) # build-in login view
]