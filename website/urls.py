from django.urls import path
from . import views_website

urlpatterns = [ 
    path('', views_website.index, name='business_funding'),
    path('careers/', views_website.careers, name='careers'),
    path('about_us/', views_website.about_us, name='about_us'),
    path('contact_us/', views_website.contact_us, name='contact_us'),
    path('faq/', views_website.faq, name='faq'),
    path('preapproval_application_1/', views_website.preapproval_application_1, name='preapproval_application_1'),
    
    
    
    
    path('milestones/', views_website.milestones, name='milestones'),
    
]