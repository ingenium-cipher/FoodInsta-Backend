from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = Member.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

# Create your views here.
