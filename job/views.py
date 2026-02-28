from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from job.models import Recruiter
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from datetime import date


def home(request):
    return render(request, 'home.html')


def admin_login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                error = "not set"
            else:
                error = "Access Denied: You do not have administrative privileges."
        else:
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
        if user is not None:
            if not user.is_staff:          # regular (non-staff) job-seeker
                login(request, user)
                error = "not set"
            else:
                error = "Access Denied: Staff accounts must login through the Admin portal."
        else:
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
            with transaction.atomic():
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
            print("Recruiter signup error:", e)
            error = "yes"
        context = {'error': error}
        return render(request, 'recruiter_signup.html', context)
    return render(request, 'recruiter_signup.html')

def user_name(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        contact = request.POST['contact']
        gender = request.POST['gender']

        student.user.first_name=f
        student.user.last_name=l
        student.mobile=contact
        student.gender=gender

        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"
        try:
            i=request.FILES['image']
            student.image=i
            student.save()
            error="no"
        except:
            pass

    context={'student':student,'error':error}
    return render(request, 'user_home.html',context)


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    recruiter_acc = Recruiter.objects.all()
    student_acc = StudentUser.objects.all()
    context = {
        'recruiter_acc':recruiter_acc,
        'student_acc':student_acc
    }
    return render(request, 'admin_home.html',context)


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    user =request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        contact = request.POST['contact']
        gender = request.POST['gender']


        recruiter.user.first_name=f
        recruiter.user.last_name=l
        recruiter.mobile=contact
        recruiter.gender=gender

        try:
            recruiter.save()
            recruiter.user.save()
            error="no"
        except:
            error="yes"
    context={'recruiter':recruiter,'error':error}
    return render(request, 'recruiter_home.html',context)


def do_logout(request):
    logout(request)
    return redirect('home')


# user signup
def user_signup(request):
    error=""
    if request.method == 'POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES.get('image')
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l,email=e)
                StudentUser.objects.create(user=user,mobile=con,gender=gen,image=i)
            error = "no"

        except Exception as e:
            print("Student signup error:", e)
            error = "yes"
        context={'error':error}
        return render(request, 'user_signup.html',context)
    return render(request, 'user_signup.html')


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    data=StudentUser.objects.all()
    context={'data':data}
    return render(request, 'view_users.html',context)


def delete_user(request,pk):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    student = User.objects.get(id=pk)
    student.delete()
    return redirect('view_users')

def delete_recruiter(request,pk):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    recruiter = User.objects.get(id=pk)
    recruiter.delete()
    return redirect('recruiter_all')


def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    data =Recruiter.objects.filter(status='pending')
    context = {'data': data}
    return render(request, 'recruiter_pending.html',context)

def recruiter_all(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    data = Recruiter.objects.all()
    context = {'data': data}
    return render(request, 'recruiter_all.html',context)


def change_status(request,pk):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    error=""
    recruiter = Recruiter.objects.get(id=pk)
    if request.method == "POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    context = {
        'recruiter':recruiter,
        'error':error
    }
    return render(request, 'change_status.html',context)


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    error = ""
    if request.method == 'POST':
        current = request.POST['currentpassword']
        new = request.POST['newpassword']
        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(current):
                user.set_password(new)
                user.save()
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
        context = {'error': error}
        return render(request, 'change_passwordadmin.html', context)
    return render(request, 'change_passwordadmin.html')
    

def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error = ""
    if request.method == 'POST':
        current = request.POST['currentpassword']
        new = request.POST['newpassword']
        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(current):
                user.set_password(new)
                user.save()
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
        context = {'error': error}
        return render(request, 'change_passworduser.html', context)
    return render(request, 'change_passworduser.html')
    


def change_passwordrecruiter(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    error=""
    if request.method == 'POST':
        current = request.POST['currentpassword']
        new = request.POST['newpassword']
        try:
            user = User.objects.get(id=request.user.id)
            if user.check_password(current):
                user.set_password(new)
                user.save()
                error="Password changed successfully"
            else:
                error="Current password is incorrect"
        except:
            error="Current password is incorrect"
    context={
        'error':error
    }
    return render(request, 'change_passwordrecruiter.html',context)



def recruiter_accept(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    data = Recruiter.objects.filter(status='approved')
    context = {'data': data}
    return render(request, 'recruiter_accept.html',context)


def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    data=Recruiter.objects.filter(status='rejected')
    context={'data':data}
    return render(request, 'recruiter_rejected.html',context)

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error=""
    if request.method == 'POST':
        jobtitle = request.POST['jobtitle']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        salary = request.POST['salary']
        skills = request.POST['skills']
        experience = request.POST['experience']
        description = request.POST['description']
        try:
            Job.objects.create(recruiter=recruiter,title=jobtitle,start_date=startdate,end_date=enddate,salary=salary,skills=skills,experience=experience,description=description)
            error="no"
        except:
            error="yes"
    context={'error':error}
    return render(request, 'add_job.html',context)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    context={'job':job}
    return render(request, 'job_list.html',context)

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    error=""
    job=Job.objects.get(id=pid)
    if request.method=='POST':
        jt=request.POST['jobtitle']
        sd=request.POST['startdate']
        ed=request.POST['enddate']
        sal=request.POST['salary']
        exp=request.POST['experience']
        skills=request.POST['skills']
        des=request.POST['description']
        
        job.title=jt
        job.salary=sal
        job.experience=exp
        job.skills=skills
        job.description=des
        
        try:
            job.save()
            error="no"
        except:
            error="yes"
        if sd:
            try:
                job.start_date=sd
                job.save()
            except:
                pass
        if ed:
            try:
                job.end_date=ed
                job.save()
            except:
                pass

    context={'error':error,'job':job}
    return render(request, 'edit_jobdetail.html',context)

def latest_jobs(request):
    job=Job.objects.all().order_by('-start_date')
    context={'job':job}
    return render(request, 'latest_jobs.html',context)


def user_latestjobs(request):
    job=Job.objects.all().order_by('-start_date')
    context={'job':job}
    return render(request, 'user_latestjobs.html',context)



def job_detail(request,pk):
    job=Job.objects.get(id=pk)
    context={'job':job}
    return render(request, 'job_detail.html',context)



def applyforjob(request,pk):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    error = ""
    user=request.user
    student = StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pk)
    date1=date.today()
    if job.end_date < date1:
        error="Job is not available"
    elif job.start_date > date1:
        error="Job is not open for application"
    else:
        if request.method == 'POST':
            resume = request.FILES['resume']
            Apply.objects.create(job=job,student=student,resume=resume, applydate=date.today())
            error = "done"
    context = {
        'error':error,
    }
    return render(request, 'applyforjob.html',context)


def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('recruiterlogin')
    
    data=Apply.objects.all()
    
    d={'data':data}
    return render(request, 'applied_candidatelist.html',d)

def contact(request):
    return render(request, 'contact.html')

    
    