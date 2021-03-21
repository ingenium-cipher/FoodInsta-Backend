from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

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