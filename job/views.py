from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from job.models import Recruiter
from django.contrib.auth import authenticate, login, logout
from datetime import date


def home(request):
    return render(request, 'home.html')


def admin_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "not set"
            else:
                error = "Invalid Login Credentials"
        except:
            error = "Invalid Login Credentials"
        context = {'error': error}
        return render(request, 'admin_login.html', context)
    return render(request, 'admin_login.html')


def user_login(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            if not user.is_staff:          # regular (non-staff) job-seeker
                login(request, user)
                error = "not set"
            else:
                error = "Invalid Login Credentials"
        except:
            error = "Invalid Login Credentials"
        context = {'error': error}
        return render(request, 'user_login.html', context)
    return render(request, 'user_login.html')


def recruiter_login(request):
    error = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status == "approved":
                    login(request, user)
                    error = "not set"
                else:
                    error = "Your account is pending approval."
            except Recruiter.DoesNotExist:
                error = "No recruiter account found for these credentials."
        else:
            error = "Invalid Login Credentials"
        context = {'error': error}
        return render(request, 'recruiter_login.html', context)
    return render(request, 'recruiter_login.html')


def recruiter_signup(request):
    error = ""
    if request.method == "POST":
        fname   = request.POST['fname']
        lname   = request.POST['lname']
        email   = request.POST['email']
        password = request.POST['password']
        contact = request.POST['contact']
        gender  = request.POST['gender']
        company = request.POST['company']
        image   = request.FILES.get('image')   # optional profile photo

        try:
            user = User.objects.create_user(
                username=email,
                password=password,
                first_name=fname,
                last_name=lname,
                email=email,
            )
            Recruiter.objects.create(
                user=user,
                mobile=contact,
                image=image,
                gender=gender,
                company=company,
                type="recruiter",
                status="pending",
            )
            error = "no"
        except Exception as e:
            error = "yes"
        context = {'error': error}
        return render(request, 'recruiter_signup.html', context)
    return render(request, 'recruiter_signup.html')