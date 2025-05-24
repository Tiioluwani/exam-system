from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Registration and authentication
    path('register/', views.register, name='register'),  # Registration view
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Logout view
]
