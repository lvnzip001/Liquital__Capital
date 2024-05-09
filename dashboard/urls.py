from django.urls import path
from . import views_dashboard

urlpatterns = [ 
    path('dashboard', views_dashboard.dashboard, name='dashboard'),
    path('data_input', views_dashboard.data_input, name='data_input'),
    path('datatable', views_dashboard.datatable, name='datatable'),
    path('view_loans', views_dashboard.view_loans, name='view_loans'),
    path('delete_loans', views_dashboard.delete_loans, name='delete_loans'),
    
    
    path('convert-to-df/<str:tbl>/', views_dashboard.submit_upload, name='submit_upload'),
    

    
    
]