# exam_system/urls.py

from django.contrib import admin
from django.urls import path, include
from exams import views as exam_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', exam_views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('exams/', include('exams.urls')),
    path('results/', include('results.urls')),

    # ⬇️ This is what you need to make sure is there:
    path('accounts/', include('accounts.urls')),  # <-- this enables /accounts/register/
]
