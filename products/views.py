from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .pagination import *
from django.utils import timezone
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class PostCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostRegisterSerializer

class PostListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostListSerializer
    pagination_class = PostListPagination

    def get_queryset(self):
        # print(self.kwargs)
        city_name = self.request.GET['city']
        city_obj = City.objects.get(name__iexact=city_name)
        return Post.objects.filter(city=city_obj, is_completed=False, product__fresh_upto__gt=timezone.now())

class PostDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostDetailSerializer

    def get_object(self):
        return get_object_or_404(Post, static_id = self.request.GET['static_id'])

class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        ordered_by = Member.objects.get(auth_user=request.user)
        post = Post.objects.get(static_id=request.data['static_id'])
        Order.objects.create(ordered_by=ordered_by, post=post)
        return Response({"message": "Order created successfully", "status": 1})
        
class UserPostListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPostListSerializer

    def get_queryset(self):
        return Post.objects.filter(member__auth_user = self.request.user)

class OrderListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserOrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(ordered_by__auth_user = self.request.user)

class RequestListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RequestListSerializer

    def get_queryset(self):
        return Order.objects.filter(post__static_id = self.request.GET['static_id'], order_status='Pending')

class UpdateOrderStatusView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        post = get_object_or_404(Post, static_id=request.data['post_static_id'])
        ordered_by = get_object_or_404(Member, static_id = request.data['ordered_by_static_id'])
        order = get_object_or_404(Order, post=post, ordered_by=ordered_by)
        if order.post.member.auth_user != request.user:
            return Response({"message": "You cannot update order status of other's post!", "status": 0})
        order.order_status = request.data['order_status'].title()
        order.save()
        return Response({"message": "Order status updated successfully", "status": 1})


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
