from django.shortcuts import redirect, render
from django.contrib.auth.models import auth
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import random
import hashlib
import hmac
import base64
from .models import EmailVerificationTokenModel
from datetime import datetime, timedelta, date
import time
from uuid import uuid4
from django.contrib.auth.hashers import make_password
from utils.mail.mail_sender import EmailVerificationMailSender
from django.conf import settings



# function based views.py
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny

from .models import User,GoogleUserPasswordModel
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

import pytz

def getTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    hour=int(current_time[0]+current_time[1])
    minute=int(current_time[3]+current_time[4])
    second=int(current_time[6]+current_time[7])
    start_time_in_seconds=(hour*60*60)*(minute*60)+second
    return start_time_in_seconds


@api_view(['POST',])
@permission_classes([AllowAny,])
def register(request):
    serializer = UserSerializer(data=request.data)
    data={}
    print("View")
    print(request.data)
    if serializer.is_valid():
        if not request.data["username"].isalnum(): 
          return JsonResponse({"error":"Username Must Only Consist Of Alphabets And Numbers. No Spaces And Special Characters Permitted"})  
        else:
          user = serializer.save()
          data['response']="successfully registered new user."
          data['email']=user.email
          data['username']=user.username
          # token = Token.objects.get(user=user).key
          # data['token'] = token
          rand_token = uuid4()
          emailVerify  = EmailVerificationTokenModel()
          emailVerify.user = user
          emailVerify.token = rand_token
          emailVerify.created_time = datetime.now()
          emailVerify.created_time_in_seconds = getTime()
          current_site = get_current_site(request).domain
          relativeLink = reverse('verify-email')
          absUrl = 'http://'+current_site+relativeLink+'?token='+str(rand_token)
          print(absUrl)
          emailVerifyUtility = EmailVerificationMailSender(user)
          emailVerifyUtility.sendUserEmailVerifyMessage(absUrl)
          emailVerify.save()
          
    else:
        data = serializer.errors
        if ('email address already exists' in str(serializer.errors)) and ('username already exists' in str(serializer.errors)):
          return JsonResponse({"error":"Username And Email Address Already Taken"})
        elif ('username already exists' in str(serializer.errors)):
          return JsonResponse({"error":"Username Already Taken"})
        elif ('email address already exists' in str(serializer.errors)):
          if User.objects.get(email=request.data["email"]).auth_type == "google":
            return JsonResponse({"error":"Email Address Already Taken. Login With Google To Continue"})
          return JsonResponse({"error":"Email Address Already Taken"})
        elif ('may not be blank' in str(serializer.errors)):
          return JsonResponse({"error":"Do Not Leave Any Field Blank"})    
        elif ('valid email address' in str(serializer.errors)):
          return JsonResponse({"error":"Enter A Valid Email Address"})   
        print(serializer.errors)
    return Response(data)


def verifyemail(request):
  token = request.GET.get('token')
  print(token)
  emailVerify = EmailVerificationTokenModel.objects.get(token=token)
  current_time = getTime()
  timeTokenCreatedPlus5Minutes = emailVerify.created_time_in_seconds + 60*5
  today = date.today()
  if today <= emailVerify.created_time.date():
    if current_time > timeTokenCreatedPlus5Minutes:
        print(current_time)
        print(timeTokenCreatedPlus5Minutes)
        return redirect(settings.ROOTURL+'/accounts/verify-email-failed')
  user= emailVerify.user
  user.is_verified=True
  user.save()
  return redirect(settings.ROOTURL+'/accounts/verify-email-success')

  



def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0,1000))
        return generate_username(random_username)


@api_view(['POST',])
@permission_classes([AllowAny,])
def checkgoogleuserexists(request):
  if User.objects.filter(email=request.data["email"]).exists():
    user = User.objects.get(email=request.data["email"])
    if user.auth_type == "email":
      return JsonResponse({"error":"You Have Already Created An Account Using Email And Password. Cannot Continue With Google"})
    else:
      return JsonResponse({"success":"User Exists"})
  else:
    return JsonResponse({"success":"User Does Not Exist"})

@api_view(['POST',])
@permission_classes([AllowAny,])
def registergoogleuser(request):
  email = request.data["email"]
  password = request.data["password"]
  passwordModel = GoogleUserPasswordModel()
  passwordModel.plain_text_password = password

  auth_type  = "google"
  user = User()
  user.email = email
  user.username = generate_username(email.split("@")[0])
  user.password = make_password(password)
  user.auth_type = auth_type
  user.is_verified = True
  user.save()
  token = Token.objects.get(user=user).key
  passwordModel.user = User.objects.get(email=email)
  user= auth.authenticate(email=request.data["email"], password=passwordModel.plain_text_password)
  auth.login(request,user)
  passwordModel.save()

  return JsonResponse({"success":"registered and logged in google user",
                      "token": token})

@api_view(['POST',])
@permission_classes([AllowAny,])
def logingoogleuser(request):
  email = request.data["email"]
  user = User.objects.get(email=email)
  token = Token.objects.get(user=user).key
  passwordModel = GoogleUserPasswordModel.objects.get(user=user)
  print(user.id)
  print(passwordModel.plain_text_password)
  user= auth.authenticate(email=request.data["email"], password=passwordModel.plain_text_password)
  auth.login(request,user)
  print(user.username)
  print(user.is_authenticated)
  return JsonResponse({"success":"logged in google user",
                        "token":token})

@api_view(['POST',])
@permission_classes([AllowAny,])
def registerlogingoogleuser(request):
    data={}
    print("View")
    print(request.data)
    if User.objects.filter(email=request.data["email"]).exists():
      user = User.objects.get(email=request.data["email"])
      if user.auth_type == "email":
        return JsonResponse({"error":"You Have Already Created An Account Using Email And Password. Cannot Continue With Google"})
      else:
        token = Token.objects.get(user=user).key
        data['response']="Logged In User"
        data['email']=user.email
        data['username']=user.username
        data['token'] = token
        return JsonResponse(data)
    else:
        userName = request.data["email"].split("@")[0]
        user = User()
        user.username = generate_username(userName)
        user.auth_type = request.data["auth_type"]
        secret = bytes("1234",encoding="utf8")
        signature = base64.b64encode(secret)
        signature = signature.decode("utf-8") 
        user.password = signature
        user.email = request.data["email"]
        user.is_verified = True
        user.save()
        token = Token.objects.get(user=user).key
        data['response']="successfully registered new user."
        data['email']=user.email
        data['username']=user.username
        data['token'] = token
        return JsonResponse(data)


  
@api_view(['GET', 'POST'])
@permission_classes([AllowAny,])
def login(request):
  data={}
  if User.objects.filter(email=request.data["email"]).exists()==False:
    return JsonResponse({"error":"Please Register First"})
  elif User.objects.filter(email=request.data["email"]).exists():
    user = User.objects.get(email=request.data["email"])
    if user.auth_type == "google":
      return JsonResponse({"error":"Email Already Linked To A Google Account. Please Login Using Your Google Account"})
    else:
      user= auth.authenticate(email=request.data["email"], password=request.data["password"])
      if user is not None:
        if not user.is_verified:
          return JsonResponse({"error":"Please Verify Your Email Address First"})
        auth.login(request,user)
        token = Token.objects.get(user=user).key
        data['response']="successfully logged in user."
        data['email']=user.email
        data['username']=user.username
        data['token'] = token
        return JsonResponse(data)
      else:
        return JsonResponse({"error":"Invalid Password"})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def snippet_list(request):
    return Response({"hello":"world"})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def checkuser(request):
    print(request.user)
    return Response({"success":"you can access",
                     "email": request.user.email,
                     "username": request.user.username,
                     "auth_type": request.user.auth_type,
                     })




'''
{
"username":"johnty",
"email":"johnty@gmail.com",
"password":"12345678"
}

{
"email":"johnty@gmail.com",
"username":"johnty",
"password":"12345678",
"auth_type":"google"
}
'''
