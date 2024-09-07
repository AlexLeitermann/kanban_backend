from datetime import datetime
from django.db import models
from django.conf import settings

# Create your models here.
class Tasks(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, default='')
    color = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None)
    priority = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f'({self.id}) {self.title}, Status: {self.status} Priority: {self.priority}'
    
class Contacts(models.Model):
    name = models.CharField(max_length=150, default='Guest')
    initials = models.CharField(max_length=2, default='G')
    email = models.CharField(max_length=250, blank=True, default='guest@example.com')
    phone = models.CharField(max_length=30, blank=True, default='+49 12 3456789')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, default=None, null=True)
    
    def __str__(self) -> str:
        return f'({self.id}) {self.name}'