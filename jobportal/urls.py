from django.contrib import admin
from django.urls import path
from job import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('adminlogin/', views.admin_login, name='adminlogin'),
    path('userlogin/', views.user_login, name='userlogin'),
    path('recruiterlogin/', views.recruiter_login, name='recruiterlogin'),
    path('recruitersignup/', views.recruiter_signup, name='recruitersignup'),
    path('usersignup/', views.user_signup, name='usersignup'),
    path('userhome/', views.user_name, name='userhome'),
    path('adminhome/', views.admin_home, name='adminhome'),
    path('recruiterhome/', views.recruiter_home, name='recruiterhome'),
    path('logout/', views.do_logout, name='logout'),
    path('view_users/', views.view_users, name="view_users"),
    path('recruiter_pending/', views.recruiter_pending, name="recruiter_pending"),
    path('recruiter_accepted/', views.recruiter_accept, name="recruiter_accepted"),
    path('recruiter_rejected/', views.recruiter_rejected, name="recruiter_rejected"),
    path('recruiter_all/', views.recruiter_all, name="recruiter_all"),
    path('change_passwordadmin/', views.change_passwordadmin, name="change_passwordadmin"),
    path('change_passworduser/', views.change_passworduser, name="change_passworduser"),
    path('change_passwordrecruiter/', views.change_passwordrecruiter, name="change_passwordrecruiter"),
    path('delete_user/<int:pk>/', views.delete_user, name="delete_user"),
    path('delete_recruiter/<int:pk>/', views.delete_recruiter, name="delete_recruiter"),
    path('change_status/<int:pk>/', views.change_status, name="change_status"),
    path('add_job/', views.add_job, name="add_job"),
    path('job_list/', views.job_list, name="job_list"),
    path('edit_jobdetail/<int:pk>/', views.edit_jobdetail, name="edit_jobdetail"),
    path('latest_jobs/', views.latest_jobs, name="latest_jobs"),
    path('user_latestjobs/', views.user_latestjobs, name="user_latestjobs"),
    path('job_detail/<int:pk>/', views.job_detail, name="job_detail"),
    path('applyforjob/<int:pk>/', views.applyforjob, name="applyforjob"),
    path('applied_candidatelist/', views.applied_candidatelist, name="applied_candidatelist"),
    path('contact/', views.contact, name="contact"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

