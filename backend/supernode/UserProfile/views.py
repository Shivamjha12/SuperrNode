from django.shortcuts import render
from rest_framework.views import *
from accounts.views import get_user_from_token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# models
from accounts.models import User
from .models import UserProfile
# serializers
from .serializers import ProfileModelSerializer

# amazon s3 bucket 
bucket_name = 'superrnode-img'
import boto3
from django.core.files.storage import default_storage
from django.conf import settings

def upload_image_to_s3(image_file):
    s3_client = boto3.client('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_S3_REGION_NAME)
    
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    file_path = f'profile/images/{image_file.name}'  
    s3_client.upload_fileobj(image_file, bucket_name, file_path)
    s3_url = f'https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}'
    return s3_url

def delete_image_from_s3(bucket_name, key):
    try:
        s3_client = boto3.client('s3')
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        return True, None
    except Exception as e:
        return False, str(e)


#views

class GetUserProfileView(APIView):
    
    def get(self, request,username):
        try:
            user = User.objects.filter(useruniquename=username).first()
            if user==None:
                return Response({"error":"User Not Found"},status=status.HTTP_404_NOT_FOUND)
            
            profile = UserProfile.objects.filter(user=user).first()
            if profile==None:
                return Response({"error":"Profile Not Found"},status=status.HTTP_404_NOT_FOUND)
            profile_data = ProfileModelSerializer(profile)
            return Response(profile_data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)

class CreateEditDeleteProfileView(APIView):
    
    def post(self, request):
        username = request.data.get('username',None)
        image    = request.data.get('image',None)
        intrests = request.data.get('intrests',None)
        bio      = request.data.get('bio',None)
        if username == None:
            return Response({"error":"Username not provided"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(useruniquename=username).first()
        if user == None:
            return Response({"error":"User Not Found"},status=status.HTTP_404_NOT_FOUND)
        is_profile_user = UserProfile.objects.filter(user=user).first()
        if is_profile_user!=None:
            return Response({"error":"User Already have Profile"},status=status.HTTP_400_BAD_REQUEST)
        else:
            profile = UserProfile.objects.create(user=user,intrests=intrests,bio=bio)
            profile.save()
            
            return Response({"profile":"Profile Created"},status=status.HTTP_200_OK)
        
    
    def put(self, request):
        uuid = request.data.get('uuid',None)
        image    =  request.FILES.get('image',None)
        interests = request.data.get('intrests',None)
        bio      = request.data.get('bio',None)
        if image==None and interests==None and bio==None:
            return Response({"Error":"No Attribute Provided"},status=status.HTTP_400_BAD_REQUEST)
        profile = UserProfile.objects.get(uuid=uuid)
        if profile !=None:
            if interests != None and bio != None and image == None:
                # Case 1: interests is not None, bio is not None, and image is None
                profile.interests = interests
                profile.bio = bio
                profile.save()
                return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)

            elif interests != None and bio == None and image != None:
                # Case 2: interests is not None, bio is None, and image is not None
                profile.interests = interests
                if profile.user_image != '':
                    key = profile.user_image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        profile.user_image = image_url
                        profile.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                image_url = upload_image_to_s3(image)
                profile.user_image = image_url
                profile.save()
                return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)

            elif interests != None and bio != None and image != None:
                # Case 3: interests is not None, bio is not None, and image is not None
                profile.interests = interests
                if profile.user_image != '':
                    key = profile.user_image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        profile.user_image = image_url
                        profile.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                profile.bio = bio
                image_url = upload_image_to_s3(image)
                profile.user_image = image_url
                profile.save()
                return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)

            elif interests == None and bio != None and image != None:
                # Case 4: interests is None, bio is not None, and image is not None
                profile.bio = bio
                if profile.user_image != '':
                    key = profile.user_image[51::]
                    success, error_message = delete_image_from_s3(bucket_name, key)
                    if success:
                        print("Image deleted successfully")
                        image_url = upload_image_to_s3(image)
                        profile.user_image = image_url
                        profile.save()
                        return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)
                    else:
                        print(f"Failed to delete image: {error_message}")
                image_url = upload_image_to_s3(image)
                profile.user_image = image_url
                profile.save()
                return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)

            elif interests == None and bio != None and image == None:
                # Case 5: interests is None, bio is not None, and image is None
                profile.bio = bio
                profile.save()
                return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)

            elif interests != None and bio == None and image == None:
                # Case 6: interests is not None, bio is None, and image is None
                profile.interests = interests
                profile.save()
                return Response({"success": "Profile updated"}, status=status.HTTP_200_OK)

        else:
            return Response({"error":"Something went wrong"},status=status.HTTP_400_BAD_REQUEST)