from django.urls import path
from . import views_auth

urlpatterns = [
    path('register/', views_auth.register, name='register'),
    path('client_login/', views_auth.client_login, name='client_login'),
]