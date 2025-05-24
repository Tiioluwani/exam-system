# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_results, name='student_results'),
    path('admin/', views.admin_results, name='admin_results'),
    path('view/<int:attempt_id>/', views.view_result, name='view_result'),
]