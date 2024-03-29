from django.db import models
from accounts.models import *
# Create your models here.
import uuid
class UserProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_image = models.URLField(blank=True,null=True)
    intrests = models.TextField(blank=True,null=True)
    bio = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return str(self.user.name) +" profile"
