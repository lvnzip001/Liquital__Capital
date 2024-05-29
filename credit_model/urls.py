from django.urls import path
from . import views_credit as views

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/',views.about_us, name = 'about_us'),
    path('registered/',views.registered, name = 'registered'),
    path('data_input/',views.data_input, name = 'data_input'),
    path('test/',views.test, name = 'test'),
    path('registered_data_input/<str:company>',views.registered_data_input, name = 'registered_data_input'),
    path('data_pdf/<str:Entity_Name>/',views.data_pdf, name = 'data_pdf'),
   
]

