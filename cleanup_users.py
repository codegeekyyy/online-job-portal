import os
import sys
import django

sys.path.append('c:\\dev\\job_portal\\django-online-job-portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
django.setup()

from django.contrib.auth.models import User
from job.models import Recruiter, StudentUser

users_to_delete = []
for u in User.objects.filter(is_superuser=False):
    if not Recruiter.objects.filter(user=u).exists() and not StudentUser.objects.filter(user=u).exists():
        print(f"Orphaned User: {u.username}")
        users_to_delete.append(u.id)

if users_to_delete:
    User.objects.filter(id__in=users_to_delete).delete()
    print(f'Deleted {len(users_to_delete)} orphaned users.')
else:
    print('No orphaned users found.')
