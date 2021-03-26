from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.shortcuts import get_object_or_404

import firebase_admin
from firebase_admin import credentials, auth
import json

class UserLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        if not firebase_admin._apps:
            cred = credentials.Certificate('google-firebase.json')
            default_app = firebase_admin.initialize_app(cred)

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

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MemberDetailSerializer

    def get_object(self):
        if 'static_id' in self.request.GET:
            return get_object_or_404(Member, static_id=self.request.GET['static_id'])
        return Member.objects.get(auth_user=self.request.user)

class CityListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CityListSerializer
    queryset = City.objects.all()

class NGOListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NGOListSerializer
    queryset = NGO.objects.all()

# Create your views here.
