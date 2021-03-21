from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *

class PostCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostRegisterSerializer

# Create your views here.
