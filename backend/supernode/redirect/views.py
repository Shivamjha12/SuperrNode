from django.shortcuts import render,redirect
from rest_framework.views import *
from accounts.views import get_user_from_token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
# models
from accounts.models import User
from Link.models import Link, LinkGroup


class LinkRedirectView(APIView):
    
    def get(self, request,username,UniqueLinkKeyword):
        try:
            user = User.objects.filter(useruniquename=username).first()
            if user==None:
                return HttpResponse("User Not Found")
            link = Link.objects.filter(user=user,uniqueName=UniqueLinkKeyword).first().url
            if link==None:
                return HttpResponse("User Doesn't have this Link, Please recheck Link Unique Keyword")
            return redirect(link)
        except Exception as e:
            return HttpResponse(f"UnExpected Error Happened: {e}")