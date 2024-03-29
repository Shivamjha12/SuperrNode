from rest_framework import serializers
from .models import *

class ProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    userfullname = serializers.CharField(source='user.name')
    class Meta:
        model = UserProfile
        fields = ('uuid','user','userfullname','bio','intrests','user_image')

    