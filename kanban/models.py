import datetime
from django.db import models
from django.conf import settings

# Create your models here.
class Tasks(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, default='')
    color = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    members = models.JSONField()
    
class Contacts(models.Model):
    name = models.CharField(max_length=150, default='Guest')
    initials = models.CharField(max_length=2, default='G')
    email = models.CharField(max_length=250, default='guest@example.com')
    phone = models.CharField(max_length=30, default='+49 12 3456789')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    
