from django.urls import path
from django.urls import include
from .views import *

urlpatterns=[
    path("login/", UserLoginView.as_view())
]