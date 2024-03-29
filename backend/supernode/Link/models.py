from django.db import models
from accounts.models import User
# Create your models here.
import uuid

class Link(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    description  = models.CharField(max_length=70)
    url          = models.URLField()
    no_of_clicks = models.IntegerField(default=0)
    uniqueName   = models.CharField(max_length=100, null=True, blank=True, unique=True)
        
    def __str__(self):
        return f"{self.description} - {self.user.name}"

class LinkGroup(models.Model):
    link_group_id = models.UUIDField(default=uuid.uuid4, editable=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    name          = models.CharField(max_length=50)
    description   = models.CharField(max_length=255)
    links         = models.ManyToManyField(Link, related_name='link_groups')
    image         = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return str(self.name)