from django.urls import path
from . import views

app_name = 'console'

urlpatterns = [
    # Vue principale de la console
    path('', views.console_view, name='dashboard'),
    
    # API endpoints
    path('api/logs/', views.search_logs, name='search_logs'),
    path('api/logs/<uuid:log_id>/', views.get_log_details, name='log_details'),
    path('api/operations/', views.get_operation_status, name='operations'),
    path('api/operations/<uuid:operation_id>/', views.get_operation_status, name='operation_details'),
] 