from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .pagination import *

class PostCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostRegisterSerializer

class PostListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostListSerializer
    pagination_class = PostListPagination
    queryset = Post.objects.filter(is_active=True)

# class GetQRImage(APIView):

#     permission_classes = (IsAuthenticated,)

#     def generate_qr_image(data):
#         student_qr = qrcode.make(data)
#         student_qr = student_qr.resize([250, 250])
#         response = HttpResponse(content_type="image/jpeg")
#         student_qr.save(response, "JPEG")
#         return response

#     def get(self, request, format=None)
#         return generate_qr_image(request.GET['qr_code'])

# Create your views here.
