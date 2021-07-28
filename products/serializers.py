from rest_framework import serializers
from .models import *
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from users.serializers import MemberDetailSerializer
import pytz

class ProductSerializer(serializers.ModelSerializer):

    fresh_upto = serializers.DateTimeField(input_formats=[settings.DATETIME_FORMAT], format=settings.DATETIME_FORMAT, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ('id', )

    def validate_fresh_upto(self, value):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, pytz.timezone(settings.TIME_ZONE))

        if value <= timezone.now():
            raise ValidationError("Food should be fresh after current time.")
        return value

    def get_image(self, obj):
        return obj.get_image_url()

class PostListSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    created_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    num_of_requests = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    author_pic = serializers.SerializerMethodField()
    author_type = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('product', 'created_at', 'static_id', 'num_of_requests', 'author_name', 'author_pic', 'author_type')
    
    def get_num_of_requests(self, obj):
        return obj.post_orders.all().count()

    def get_author_name(self, obj):
        return obj.member.get_name()

    def get_author_pic(self, obj):
        return obj.member.get_profile_pic_url()

    def get_author_type(self, obj):
        return obj.member.member_type

class PostDetailSerializer(PostListSerializer):

    member = MemberDetailSerializer()
    request_status = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        model = Post
        fields = PostListSerializer.Meta.fields + ('member', 'location', 'address', 'request_status', 'contact_no')

    def get_request_status(self, obj):
        order = obj.post_orders.filter(ordered_by__auth_user = self.context['request'].user)
        if order.exists():
            return order[0].order_status
        return None

class PostRegisterSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    city = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = Post
        fields = ('product', 'address', 'location', 'city', 'contact_no')
    
    def create(self, validated_data):
        product_data = validated_data.pop('product')
        member = Member.objects.filter(auth_user=self.context['request'].user)[0]
        city_obj = member.city
        if 'city' in validated_data:
            city_name = validated_data.pop('city')
            city_qs = City.objects.filter(name=city_name)
            if city_qs.exists():
                city_obj = city_qs[0]
            else:
                city_obj = City.objects.create(name=city_name)
        product = Product.objects.create(**product_data)
        post = Post.objects.create(product=product, member = member, city=city_obj, **validated_data)
        return post

class UserPostListSerializer(serializers.ModelSerializer):
    
    num_of_requests = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    post_status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('num_of_requests', 'weight', 'image', 'post_status', 'static_id')

    def get_num_of_requests(self, obj):
        return obj.post_orders.all().count()

    def get_weight(self, obj):
        return obj.product.weight

    def get_image(self, obj):
        return obj.product.get_image_url()

    def get_post_status(self, obj):
        if obj.is_deleted:
            return 'Removed'
        if obj.is_completed:
            return 'Finished'

        value = obj.product.fresh_upto
        if timezone.is_naive(value):
            value = timezone.make_aware(value, pytz.timezone(settings.TIME_ZONE))

        if value <= timezone.now():
            return 'Expired'
        return None 

class UserOrderListSerializer(serializers.ModelSerializer):

    ordered_to = serializers.SerializerMethodField()
    created_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('ordered_to', 'created_time', 'order_status', 'image')

    def get_ordered_to(self, obj):
        return obj.post.member.get_name()

    def get_image(self, obj):
        return obj.post.product.get_image_url()

class RequestListSerializer(serializers.ModelSerializer):

    ordered_by = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    member_type = serializers.SerializerMethodField()
    member_static_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('ordered_by', 'profile_pic', 'member_type', 'member_static_id')

    def get_ordered_by(self, obj):
        return obj.ordered_by.get_name()

    def get_profile_pic(self, obj):
        return obj.ordered_by.get_profile_pic_url()

    def get_member_type(self, obj):
        return obj.ordered_by.member_type

    def get_member_static_id(self, obj):
        return obj.ordered_by.static_id


    