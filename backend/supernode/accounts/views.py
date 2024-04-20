from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
import jwt,datetime
from rest_framework import generics
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from rest_framework import status
#imports related to email verification
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from supernode import settings
from django.utils import timezone
from django.utils.http import base36_to_int
from Link.models import LinkGroup
from UserProfile.models import UserProfile

def extract_timestamp_from_token(token):
    try:
        # Split the token into its parts
        parts = token.split("-")
        if len(parts) != 2:
            raise ValueError("Invalid token format")
        # Extract the timestamp from the second part of the token
        timestamp_hex = parts[1]
        # Convert the hexadecimal timestamp to an integer
        timestamp_int = int(timestamp_hex, 16)
        # Convert the integer timestamp to a string
        timestamp_str = str(timestamp_int)
        # Parse the string timestamp to a datetime object
        timestamp = timezone.datetime.utcfromtimestamp(int(timestamp_str))
        return timestamp
    except (ValueError, IndexError):
        return None





def get_user_from_token(JWTUser):
    token = None
    if JWTUser!='None':
        token = JWTUser
    # request.COOKIES.get('jwt')
    print(type(token),"typeeeeeeeeeeeeeeeeeeeeeeeeee")
    print(token,"Here is the token, -----------sssssssssssss-----s-s--s-s-sssssssss")
    if not token:
        return ('Unauthenticated please login')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return ('Unauthenticated please login')
    user = User.objects.filter(id=payload['id']).first()
    return user

def password_reset_done_page(request):
    return render(request,'registration/passwordResetDone.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return HttpResponse('registration/confirmation_success.html')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')
    
class register(APIView):
    def post(self,request):
        serializers = UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        # from here we start process of sending email to the user to verify their email
        userEmail = request.data['email']
        USER = User.objects.filter(email=userEmail).first()
        USER.is_active = False
        USER.save()
        # profile = UserProfile.objects.create(user=USER)
        # profile.save()
        linklistobj = LinkGroup.objects.create(user=USER,name="Home",description=USER.name)
        linklistobj.save()
        #1 we need to generate a token and mail content for the user
        current_site = get_current_site(request)
        mail_subject = "Activate your account"
        message =render_to_string('registration/activation_email.html',{
            'user': USER,
            'domain': current_site,
            'uid': force_str(urlsafe_base64_encode(force_bytes(USER.pk))),
            'token': account_activation_token.make_token(USER),
            
        })
        print(message)
        to_email = userEmail
        try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
                )
                print("The link has been sent to your email id to activate your account. please check your inbox and if its not there check your spam as well.")
                return Response("The link has been sent to your email", status=200)
        except Exception as e:
            User.objects.delete_user(userEmail)
            return Response(f"Something happened Wrong, Pleae Try Again {e}", status=400)
        
        return Response(serializers.data)
    
class forgotPassword(APIView):
    def post(self, request):
        userEmail = request.data['email']
        user = None
        try:
            user = User.objects.filter(email=userEmail).first()
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if user is not None:
            current_site = get_current_site(request)
            token = account_activation_token.make_token(user)
            uid = force_str(urlsafe_base64_encode(force_bytes(user.pk)))
            link_generator = f'http://{current_site}/reset/{uid}/{token}'
            print(link_generator)
            mail_subject = f"Reset your password on {current_site}"
            message =render_to_string('registration/forgot_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
                
            })
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [userEmail],
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
                )
                print("The link has been sent to your email id to activate your account. please check your inbox and if its not there check your spam as well.")
                return Response("The link has been sent to your email", status=200)
            except Exception as e:
                User.objects.delete_user(userEmail)
                return Response(f"Something happened Wrong, Pleae Try Again {e}", status=400)
        else:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

def resetPassword(request,uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('newPassword')
            confirm_password = request.POST.get('confirmPassword')
            # token_parts = token.split('-')
            # token_timestamp = float(token_parts[-1])
            testingvalue =  extract_timestamp_from_token(token)
            print("---------------Hello World----------------> ",testingvalue)
            # print(token_timestamp)
            if new_password == confirm_password:
                user.set_password(confirm_password)
                user.save()
                return redirect('password_reset_done')
            else:
                pass
        return render(request,'registration/forgotForm.html')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or link is already Used! Try To Login')
    
class login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('You are not registered on the platform')
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')
        if user.is_active==False:
             raise AuthenticationFailed('Please verify your email first to login. Check your email for the verification link.')
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=720),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        # .decode('utf-8')
        response = Response()
        # response.set_cookie(key='jwt',value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        return response

class userView(APIView):
    def get(self, request,JWTUser):
        token = None
        if JWTUser!='None':
            token = JWTUser
        # request.COOKIES.get('jwt')
        print(type(token),"typeeeeeeeeeeeeeeeeeeeeeeeeee")
        print(token,"Here is the token, -----------sssssssssssss-----s-s--s-s-sssssssss")
        if not token:
            raise AuthenticationFailed('Unauthenticated please login')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated please login')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)

class logout(APIView):
    def post(self, request):
        response = Response()
        # response.delete_cookie('jwt')
        response.data = {
            'message':"Successfully Logout"
        }
        return response