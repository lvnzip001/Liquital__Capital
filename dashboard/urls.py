from django.urls import path
from . import views_dashboard

urlpatterns = [ 
    path('dashboard', views_dashboard.dashboard, name='dashboard'),
    path('data_input', views_dashboard.data_input, name='data_input'),
    

    
    
]