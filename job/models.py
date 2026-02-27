from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=15, null=True)
    type = models.CharField(max_length=15, null=True)
    def __str__(self):
        return self.user.username

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=15, null=True)
    company = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=15, null=True)
    def __str__(self):
        return self.user.username

class Job(models.Model):
    title = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField()
    title = models.CharField(max_length=100, null=True)
    salary = models.FloatField(max_length=20)
    description = models.CharField(max_length=300, null=True)
    experience = models.CharField(max_length=100, null=True)
    skills = models.CharField(max_length=100, null=True)
    creationdate = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title


class Apply(models.Model):
    job=models.ForeignKey(Job, on_delete=models.CASCADE)
    student=models.ForeignKey(StudentUser, on_delete=models.CASCADE)
    resume=models.FileField(null=True)
    applydate=models.DateField()
    def _str_(self):
        return self.id