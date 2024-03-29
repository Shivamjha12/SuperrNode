from django.db import models
from accounts.models import *
from Link.models import *
from UserProfile.models import *
import uuid

class LinkAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_clicks = models.IntegerField(default=0)
    expression = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    
    

class LinkGroupAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_clicks = models.IntegerField(default=0)
    expression = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    linklist = models.ForeignKey(LinkGroup, on_delete=models.CASCADE)

class UserAnalytics(models.Model):
    pass
