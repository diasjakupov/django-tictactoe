from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate

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
        
