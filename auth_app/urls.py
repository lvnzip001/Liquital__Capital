from django.urls import path
from . import views_auth

urlpatterns = [
    path('register_client/', views_auth.register_client, name='register_client'),
    path('login_client/', views_auth.login_client, name='login_client'),
    path('login_client/', views_auth.login_client, name='login_client'),
    
]