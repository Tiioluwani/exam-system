# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_exams, name='admin_exams'),
    path('student/', views.student_exams, name='student_exams'),
    path('attempt/<int:exam_id>/', views.attempt_exam, name='attempt_exam'),
]

