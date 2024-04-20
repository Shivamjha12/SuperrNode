from django.shortcuts import render
from rest_framework.views import *
from accounts.views import get_user_from_token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# models
from accounts.models import User
from .models import Link, LinkGroup
#serializer
from .serializers import LinkModelSerializer,LinkGroupModelSerializer,SpecificLinkGroupModelSerializer

#amazon s3 bucket
import boto3
from django.core.files.storage import default_storage
from django.conf import settings
from UserProfile.views import bucket_name
from UserProfile.views import upload_image_to_s3
from UserProfile.views import delete_image_from_s3


class LinkGetView(APIView):
    
    def get(self,request,id):
        # this function help us to get a particular link for a user
        if id is None:
            return Response({"error":"id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            link = Link.objects.get(uuid=id)
            # Here we create serializer for link model object and pass data to serializer
            # and then pass it to client for compatiable object type(json)
            link_data = LinkModelSerializer(link)
            return Response(link_data.data)
        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

class LinkCreateEditDeleteView(APIView):
    
    def post(self, request):
        # this function takes post request from client side for creating a link for user
        # get field data from request
        jwt_token = request.data.get('jwt',None)
        description = request.data.get('description',None)
        url = request.data.get('url',None)
        if jwt_token is None:
            return Response({'error':'token is required'},status=status.HTTP_400_BAD_REQUEST)
        if description is None:
            return Response({'error':'Description is required'},status=status.HTTP_400_BAD_REQUEST)
        if url is None:
            return Response({'error':'URL is required'},status=status.HTTP_400_BAD_REQUEST)
        jwt_token_user = get_user_from_token(jwt_token)
        
        if jwt_token_user is None:
            return Response({'error':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        # create link
        try:
            link = Link.objects.create(user=jwt_token_user,description=description,url=url)
            link.save()
        except Exception as e:
            return Response({'error':f'{e}'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'Link created'},status=status.HTTP_200_OK)
    
    
    
    def put(self,request):
        # this function help us to update a particular link for a user
        id = request.data.get('id',None)
        jwt = request.data.get('jwt',None)
        description = request.data.get('description',None)
        url = request.data.get('url',None)
        if jwt == None:
            return Response({"error":"user token is required"},status=status.HTTP_400_BAD_REQUEST)
        user = get_user_from_token(jwt)
        
        if id==None:
            return Response({"error":"id is required"},status=status.HTTP_400_BAD_REQUEST)
        if description==None and id != None and url != None:
            try:
                link = Link.objects.get(uuid=id)
                if link.user != user:
                    return Response({"error":"You are not authorized to update this link"},status=status.HTTP_401_UNAUTHORIZED)
                link.url = url
                link.save()
                return Response({"success":"Link updated"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        if url==None and description != None and id != None:
            try:
                link = Link.objects.get(uuid=id)
                if link.user != user:
                    return Response({"error":"You are not authorized to update this link"},status=status.HTTP_401_UNAUTHORIZED)
                link.description = description
                link.save()
                return Response({"success":"Link updated"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        if url!=None and description!=None and id!=None:
            try:
                link = Link.objects.get(uuid=id)
                if link.user != user:
                    return Response({"error":"You are not authorized to update this link"},status=status.HTTP_401_UNAUTHORIZED)
                link.description = description
                link.url = url
                link.save()
                return Response({"success":"Link updated"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        # this function help us to delete a particular link for a user
        id = request.data.get('id',None)
        jwt = request.data.get('jwt',None)

        if id==None or jwt==None:
            return Response({"error":"id or jwt is not provided"},status=status.HTTP_400_BAD_REQUEST)
        user = get_user_from_token(jwt)
        if user==None:
            return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        try:
            link = Link.objects.get(uuid=id)
            if link.user != user:
                return Response({"error":"You are not authorized to delete this link"},status=status.HTTP_401_UNAUTHORIZED)
            link.delete()
            return Response({"success":"Link deleted"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

class UserLinkView(APIView):
    
    def get(self, request,username):
        user = User.objects.filter(useruniquename=username).first()
        if user == None:
            return Response({"error":"USER NOT FOUND"}, status=status.HTTP_400_BAD_REQUEST)
        userLinks = Link.objects.filter(user=user,is_in_linkGroup=False)
        if userLinks==None:
            return Response({"error":"LINKS NOT FOUND"}, status=status.HTTP_400_BAD_REQUEST)
        userLinksData = LinkModelSerializer(userLinks,many=True)
        # add pagination here ---<>---
        return Response(userLinksData.data)


class UserLinklistListView(APIView):
    
    def get(self, request,username):
        user = User.objects.filter(useruniquename=username).first()
        if user is None:
            return Response({"error":"User not found"},status=status.HTTP_400_BAD_REQUEST)
        userlinklists = LinkGroup.objects.filter(user=user).exclude(name="Home")
        print(userlinklists,"Here--------<1>----------------")
        data = LinkGroupModelSerializer(userlinklists,many=True)
        return Response(data.data, status=status.HTTP_200_OK) 
    
class LinklistView(APIView):
    
    def get(self, request,id):
        userlinklists = LinkGroup.objects.get(link_group_id=id)
        print(userlinklists,"Here--------<1>----------------")
        data = SpecificLinkGroupModelSerializer(userlinklists)
        return Response(data.data, status=status.HTTP_200_OK)
    
#create/update/delete of linkGroup
class LinklistCreateEditDeleteView(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            jwt = request.data.get('jwt',None)
            name = request.data.get('name',None)
            description = request.data.get('description',None)
            # link_id = request.data.get('link_id',None)
            image = request.FILES.get('image',None)
            user = get_user_from_token(jwt)
            if user is None:
                return Response({"error":"User Not Found or Invalid Token"},status=status.HTTP_400_BAD_REQUEST)
            if name==None or description==None:
                return Response({"error":"name or description or link_id is not provided"},status=status.HTTP_400_BAD_REQUEST)
            # link_object = Link.objects.get(uuid=link_id)
            # if link_object==None:
            #     return Response({"error":"Link Not Found"},status=status.HTTP_400_BAD_REQUEST)
            try:
                if image!=None:
                    image_url = upload_image_to_s3(image)
                    linklist_object = LinkGroup.objects.create(name=name,description=description,user=user,image=image_url)
                    linklist_object.save()
                    return Response({"id":f"{ linklist_object.link_group_id}"},status=status.HTTP_200_OK)
                else:
                    linklist_object = LinkGroup.objects.create(name=name,description=description,user=user)
                    linklist_object.save()
                    return Response({"id":f"{ linklist_object.link_group_id}"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        

    def put(self, request):
        jwt = request.data.get('jwt',None)
        linklist_id = request.data.get('linklist_id',None)
        name = request.data.get('name',None)
        description = request.data.get('description',None)
        image = request.FILES.get('image',None)
        
        if jwt==None:
            return Response({"error":"jwt or name or description is not provided"},status=status.HTTP_400_BAD_REQUEST)
        user = get_user_from_token(jwt)
        if user==None:
            return Response({"error":"User Not Found"},status=status.HTTP_400_BAD_REQUEST)
        linklistobj = LinkGroup.objects.get(link_group_id=linklist_id)
        if linklistobj==None:
            return Response({"error":"Linklist Not Found"},status=status.HTTP_400_BAD_REQUEST)
        if linklistobj.user!=user:
            return Response({"error":"You are not authorized to update this linklist"},status=status.HTTP_401_UNAUTHORIZED)
        try:
            if name != None and description == None and image == None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                linklistobj.name = name
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

            if name == None and description != None and image == None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                linklistobj.description = description
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

            if name == None and description == None and image != None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                
                if linklistobj.image != '':
                    key = linklistobj.image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        linklistobj.image = image_url
                        linklistobj.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                
                image_url = upload_image_to_s3(image)
                linklistobj.image = image_url
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

            if name != None and description != None and image == None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                
                linklistobj.name = name
                linklistobj.description = description
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

            if name != None and description == None and image != None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                
                
                if linklistobj.image != '':
                    key = linklistobj.image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        linklistobj.name = name
                        linklistobj.image = image_url
                        linklistobj.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                
                
                image_url = upload_image_to_s3(image)
                linklistobj.name = name
                linklistobj.image = image_url
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

            if name == None and description != None and image != None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                
                if linklistobj.image != '':
                    key = linklistobj.image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        linklistobj.description = description
                        linklistobj.image = image_url
                        linklistobj.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                
                
                image_url = upload_image_to_s3(image)
                linklistobj.description = description
                linklistobj.image = image_url
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

            if name != None and description != None and image != None:
                if linklistobj == None:
                    return Response({"error": "Linklist Not Found"}, status=status.HTTP_400_BAD_REQUEST)
                if linklistobj.image != '':
                    key = linklistobj.image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        linklistobj.name = name
                        linklistobj.description = description
                        linklistobj.image = image_url
                        linklistobj.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                        
                image_url = upload_image_to_s3(image)
                linklistobj.name = name
                linklistobj.description = description
                linklistobj.image = image_url
                linklistobj.save()
                return Response({"success": "Linklist updated"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id = request.data.get('id',None)
        jwt = request.data.get('jwt',None)

        if id==None or jwt==None:
            return Response({"error":"id or jwt is not provided"},status=status.HTTP_400_BAD_REQUEST)
        user = get_user_from_token(jwt)
        if user==None:
            return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        try:
            linklistobj = LinkGroup.objects.get(link_group_id=id)
            if linklistobj.user != user:
                return Response({"error":"You are not authorized to delete this link"},status=status.HTTP_401_UNAUTHORIZED)
            linklistobj.delete()
            return Response({"success":"Link removed"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
    
# adding/removing links to link group
class LinklistAddLinkView(APIView):
    
    def post(self, request):
        link_id = request.data.get('id',None)
        linklist_id = request.data.get('linklist_id',None)
        jwt = request.data.get('jwt',None)
        user = get_user_from_token(jwt)
        if user==None:
            return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        if link_id==None or linklist_id==None:
            return Response({"error":"link_id or linklist_id is not provided"},status=status.HTTP_400_BAD_REQUEST)
        link = Link.objects.get(uuid=link_id)
        link.is_in_linkGroup = True
        linklist = LinkGroup.objects.get(link_group_id=linklist_id)
        links_in_linklist = linklist.links.all()
        print("[[[[[[[[[[]]]]]]]]]]",links_in_linklist," the type is-->",type(links_in_linklist))
        if link in links_in_linklist:
            print("Link is already in linklist")
            return Response({"message":"Link Already in Linklist"},status=status.HTTP_400_BAD_REQUEST)
        if link==None or linklist==None:
            return Response({"error":"Link or Linklist Not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        if linklist.user!=user:
            return Response({"error":"You are not authorized to add link to this linklist"},status=status.HTTP_401_UNAUTHORIZED)
        
        linklist.links.add(link)
        return Response({"success":"Link added to linklist"},status=status.HTTP_200_OK)

class LinklistRemoveLinkView(APIView):
    
    def post(self, request):
        link_id = request.data.get('id',None)
        linklist_id = request.data.get('linklist_id',None)
        jwt = request.data.get('jwt',None)
        user = get_user_from_token(jwt)
        if user==None:
            return Response({"error":"Invalid token"},status=status.HTTP_400_BAD_REQUEST)
        if link_id==None or linklist_id==None:
            return Response({"error":"link_id or linklist_id is not provided"},status=status.HTTP_400_BAD_REQUEST)
        link = Link.objects.get(uuid=link_id)
        linklist = LinkGroup.objects.get(link_group_id=linklist_id)
        if link==None or linklist==None:
            return Response({"error":"Link or Linklist Not Found"},status=status.HTTP_400_BAD_REQUEST)
        if linklist.user!=user:
            return Response({"error":"You are not authorized to add link to this linklist"},status=status.HTTP_401_UNAUTHORIZED)
        linklist.links.remove(link)
        return Response({"success":"Link removed from linklist"},status=status.HTTP_200_OK)
    
    

