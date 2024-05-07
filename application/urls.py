from django.urls import path
from . import views_applications

urlpatterns = [ 
    path('section_0/', views_applications.section0, name='section_0'),
    path('section_1/', views_applications.company_information_view, name='section_1'),
    path('section_2/', views_applications.managing_director_view, name='section_2'),
    path('section_3/', views_applications.off_taker_details_view, name='section_3'),
    path('section_4/', views_applications.contract_information_view, name='section_4'),
    path('section_5/', views_applications.invoice_information_view, name='section_5'),
    path('section_6/', views_applications.section6, name='section_6'),
    path('section_7/', views_applications.section7, name='section_7'),
    path('section_8/', views_applications.section8, name='section_8'),
    path('section_9/', views_applications.section9, name='section_9'),
    path('section_10/', views_applications.section10, name='section_10'),
    path('section_11/', views_applications.section11, name='section_11'),
    path('section_12/', views_applications.asset_liability_view, name='asset_liability_view'),
    path('section_13/', views_applications.section13, name='section_13'),
    path('complete_application/', views_applications.complete_application, name='complete_application'),
    
    
]