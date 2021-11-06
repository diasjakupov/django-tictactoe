from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username=request.data["username"]
        password=request.data["password"]
        #{
        #    "username":"admin",
        #    "password":"admin"
        #}
        user=authenticate(username=username, password=password)
        if user is not None:
            data={"userId": user.id, "login": True, "errors":""}
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data={"userId": -1, "login": False, "errors":"No such user"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        username=request.data["username"]
        password=request.data["password"]
        if len(username)>2:
            user=User.objects.create(username=username, password=password)
            token=Token.objects.create(user=user)
            return Response(data={"userId": user.id, "token": token.key, "errors":""}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"userId": None, "token":None, "errors": "passwords are not identical or username is not correct"}, status=status.HTTP_400_BAD_REQUEST)


        
