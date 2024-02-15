from django.db import models
from accounts.models import User
# Create your models here.

class LinkList(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)

class Links(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    tags = models.TextField()
    unique_name = models.CharField(max_length=255,unique=True)
    date = models.DateTimeField(auto_now_add=True)
    linklists = models.ManyToManyField(LinkList, related_name='Links',null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title


