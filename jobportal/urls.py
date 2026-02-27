from django.contrib import admin
from django.urls import path
from job import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('adminlogin/', views.admin_login, name='admin_login'),
    path('userlogin/', views.user_login, name='user_login'),
    path('recruiterlogin/', views.recruiter_login, name='recruiter_login'),
    path('recruitersignup/', views.recruiter_signup, name='recruiter_signup'),
]
