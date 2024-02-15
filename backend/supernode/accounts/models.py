from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

class User(AbstractUser):
    name     = models.CharField(max_length=30)
    email    = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    _is_paid_user = models.BooleanField(default=False)
    username = None
    
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()
        
    @property
    def is_paid_user(self):
        return self._is_paid_user

    @is_paid_user.setter
    def is_paid_user(self, value):
        self._is_paid_user = value
        
            
    