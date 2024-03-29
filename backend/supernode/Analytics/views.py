from django.shortcuts import render,HttpResponse
from rest_framework.views import *
from accounts.views import get_user_from_token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# models
from accounts.models import User
from .models import Link, LinkGroup

class LinkClick(APIView):
    
    def get(self, request):
        uuid = request.GET.get('id',None)
        try:
            if uuid == None:
                return HttpResponse("id not found", status=404)
            link = Link.objects.get(uuid=uuid)
            if link==None:
                return HttpResponse("Link not found", status=404)
            link.no_of_clicks+=1
            link.save()

        except Exception as e:
            return HttpResponse(f"Unexpected Error Happened: {e}", status=400)

class LinkGroupClick(APIView):
    
    def get(self, request):
        uuid = request.GET.get('id',None)
        try:
            if uuid == None:
                return HttpResponse("id not found", status=404)
            link = LinkGroup.objects.get(link_group_id=uuid)
            if link==None:
                return HttpResponse("Link not found", status=404)
            link.no_of_clicks+=1
            link.save()

        except Exception as e:
            return HttpResponse(f"Unexpected Error Happened: {e}", status=400)
