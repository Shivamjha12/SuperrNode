from rest_framework import serializers
from .models import *

class LinkModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    class Meta:
        model = Link
        fields = ('uuid','description','user','url','no_of_clicks','uniqueName')

class LinkGroupModelSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source="user.useruniquename")
    userfullname = serializers.CharField(source="user.name")
    user = serializers.CharField(source="user.email")
    # links = LinkModelSerializer(many=True, read_only=True)
    # serializers.CharField(source="links.all")
    class Meta:
        
        model = LinkGroup
        fields = ('link_group_id','userfullname','user','name','description','image')
        
        
class SpecificLinkGroupModelSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source="user.useruniquename")
    userfullname = serializers.CharField(source="user.name")
    user = serializers.CharField(source="user.email")
    links = LinkModelSerializer(many=True, read_only=True)
    # serializers.CharField(source="links.all")
    class Meta:
        
        model = LinkGroup
        fields = ('link_group_id','userfullname','links','user','name','description','image')