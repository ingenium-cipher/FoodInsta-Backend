from rest_framework import serializers
from .models import *
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

class ProductSerializer(serializers.ModelSerializer):

    fresh_upto = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_fresh_upto(self, value):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, pytz.timezone(settings.TIME_ZONE))

        if value <= timezone.now():
            raise ValidationError("Food should be fresh after current time.")
        return value

class PostRegisterSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = Post
        fields = ('product', 'address', 'location')
    
    def create(self, validated_data):
        product_data = validated_data.pop('product')
        member = Member.objects.filter(auth_user=self.context['request'].user)[0]
        product = Product.objects.create(**product_data)
        post = Post.objects.create(product=product, member = member, **validated_data)
        return post

class PostListSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = Post
        fields = ('product', 'address', 'location', 'created_at')