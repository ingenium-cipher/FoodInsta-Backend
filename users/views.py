from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *

import firebase_admin
from firebase_admin import credentials, auth
import json

class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        if not firebase_admin._apps:
            cred = credentials.Certificate('google-firebase.json')
            default_app = firebase_admin.initialize_app(cred)

        print(request.body)
        data = json.loads(request.body)
        if "firebase_id" in data:
            firebase_id = data['firebase_id']
        else:
            return Response({'message': 'Insufficient Request Parameters.', "status": 0})

        try:
            user = auth.get_user(firebase_id)
            member = Member.objects.filter(auth_user__email=user.email)

            if not member.exists():
                return Response({"message": "Please register first.", "status": 2})

            # if the member exists for the email
            member = member[0]
            if not member.auth_user:
                return Response({"message": "Couldn't get access token", "status": 0})

            refresh = RefreshToken.for_user(member.auth_user)
            return Response({
                'access': str(refresh.access_token), 'refresh': str(refresh), "status": 1})

        except Exception as e:
            return Response({"message": str(e), "status": 0})

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
