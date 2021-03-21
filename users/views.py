from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class IndividualRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = IndividualRegisterSerializer

class RestaurantRegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RestaurantRegisterSerializer

class NGORegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = NGORegisterSerializer

# Create your views here.
