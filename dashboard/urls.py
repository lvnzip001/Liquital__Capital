from django.urls import path
from . import views_dashboard

urlpatterns = [ 
    path('dashboard', views_dashboard.dashboard, name='dashboard'),
    path('data_input_analysis', views_dashboard.data_input_analysis, name='data_input_analysis'),
    path('datatable', views_dashboard.datatable, name='datatable'),
    path('view_loans', views_dashboard.view_loans, name='view_loans'),
    path('delete_loans', views_dashboard.delete_loans, name='delete_loans'),
    path('analysis_table', views_dashboard.analysis_table, name='analysis_table'),
    path('analysis_charts', views_dashboard.analysis_charts, name='analysis_charts'),
    
    
    
    
    path('convert-to-df/<str:tbl>/', views_dashboard.submit_upload, name='submit_upload'),
    

    
    
]